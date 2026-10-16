# -*- coding: utf-8 -*-
"""
Robô de vigilância da legislação do ENADE e da PND.
Lê DUAS fontes oficiais e junta tudo que for de ENADE/PND (sem perder nada):
  1) INEP — páginas de legislação (ENADE e PND), via as sub-páginas que o curl lê.
  2) MEC  — mecnormas (API /pesquisa/api/atos), filtrando pelos assuntos
            "ENADE" (153153) e "Prova Nacional Docente - PND" (164503).
Monta a lista COMPLETA de atos (atos.json, mostrada na aba "Legislação" do painel)
e registra as NOVIDADES da semana (novidades_auto.json, aba "Novidades").
Só biblioteca padrão do Python. Roda no GitHub Actions.
"""
import json, re, io, os, gzip, urllib.request, datetime

INEP_URLS = [
 "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/enade/2026",
 "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/enade/2025",
 "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/prova-nacional-docente/2026-1",
 "https://www.gov.br/inep/pt-br/centrais-de-conteudo/legislacao/prova-nacional-docente/2025",
]
MEC_ASSUNTOS = {"ENADE": 153153, "PND": 164503}   # ids de assunto no mecnormas
def mec_url(aid, page=1):
    return ("https://mecnormas.mec.gov.br/pesquisa/api/atos"
            "?exata=false&ordenacao=2&sistema=1&pageSize=40&currentPage=%d&assunto=%d" % (page, aid))

ANO_MIN = 2025                      # ciclo atual (matrizes de licenciatura saíram em 2025)
ATOS = "atos.json"                 # lista completa atual de atos ENADE/PND (para o painel)
NOVI_AUTO = "novidades_auto.json"  # novidades detectadas (aba Novidades)

INCLUI = re.compile(r"edital|portaria|retifica", re.I)
EXCLUI = re.compile(r"medicina|enamed|rede nacional de certificadores|\bRNC\b|"
                    r"interlocutores do enem|chamada p[uú]blica|resultados da chamada|colaboradores|"
                    r"exame nacional do ensino m[eé]dio|\benem\b|\bsaeb\b|celpe-?bras|revalida|encceja", re.I)
RELEV  = re.compile(r"enade|prova nacional docente|\bpnd\b|forma[cç][aã]o geral|"
                    r"licenciatura|docente|agronomia|enfermagem|pedagogia|computa[cç][aã]o", re.I)
# matrizes/diretrizes de componente específico: manter só as dos nossos cursos (as de
# outras licenciaturas/bacharelados — Letras, Dança, Química etc. — são ruído para a SETREM)
MATRIZ = re.compile(r"componentes? espec[ií]ficos?|matriz de refer[eê]ncia|diretrizes de prova", re.I)
# os 7 cursos da SETREM (cada um avaliado no seu ano do ciclo) + Formação Geral (comum)
NOSSOS = re.compile(r"pedagogia|engenharia de computa[cç][aã]o|\bagronomia\b|enfermagem|"
                    r"psicologia|administra[cç][aã]o|\bdireito\b|forma[cç][aã]o geral", re.I)
MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()

def incluir(a):
    txt = (a["titulo"] + " " + a.get("ementa", "")).strip()
    if EXCLUI.search(txt):
        return False
    ano = int(a["iso"][:4]) if a["iso"] else None
    if ano is not None and ano <= 2024:
        return False
    if ano == 2025:                             # ciclo 2025: só as 2 matrizes de licenciatura ainda vigentes dos nossos (315 Docente, 331 Pedagogia)
        return bool(MATRIZ.search(txt) and re.search(r"pedagogia|forma[cç][aã]o geral docente", txt, re.I))
    if MATRIZ.search(txt):                       # matriz de curso (2026+): só a dos nossos cursos
        return bool(NOSSOS.search(txt))
    return bool(RELEV.search(txt))               # editais, retificações e atos gerais de ENADE/PND (2026+)

def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"})
    try:
        r = urllib.request.urlopen(req, timeout=60)
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return raw.decode("utf-8", "replace")
    except Exception as e:
        print("  ! falha ao ler", u[:70], "->", e)
        return ""

def datas(titulo, datestr=None):
    m = re.search(r"(\d{1,2}) de (\w+) de (\d{4})", titulo or "")
    if m:
        try:
            d, mo, y = int(m.group(1)), MESES.index(m.group(2).lower())+1, int(m.group(3))
            return ("%02d/%02d/%d" % (d, mo, y), "%04d-%02d-%02d" % (y, mo, d))
        except Exception:
            pass
    if datestr:
        m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", datestr)
        if m:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return ("%02d/%02d/%d" % (d, mo, y), "%04d-%02d-%02d" % (y, mo, d))
    return ("", "")

def chave(titulo):
    t = (titulo or "").lower()
    tm = re.search(r"\b(edital|portaria)\b", t)
    nm = re.search(r"n[ºo°]?\s*([\d.]+)", t)
    am = re.search(r"\b(20\d{2})\b", t)
    if tm and nm and am and not t.strip().startswith("retifica"):
        return "%s-%s-%s" % (tm.group(1), nm.group(1).replace(".", ""), am.group(1))
    return None

def mkato(titulo, link, fonte, ementa="", datestr=None):
    disp, iso = datas(titulo, datestr)
    k = chave(titulo) or re.sub(r"\s+", " ", (titulo or "").lower()).strip()[:90]  # título normalizado p/ deduplicar retificações
    return {"key": k, "d": disp, "iso": iso,
            "titulo": re.sub(r"\s+", " ", titulo).strip()[:200],
            "link": link, "fonte": fonte, "ementa": (ementa or "").strip()[:220]}

def from_inep():
    out, ok = [], 0
    for u in INEP_URLS:
        h = fetch(u)
        if h:
            ok += 1
        for m in re.finditer(r'href="(https?://[^"]*in\.gov\.br/[^"]+)"[^>]*>([^<]{6,220})<', h):
            link = m.group(1).strip().replace("in.gov.br/en/web/dou", "in.gov.br/web/dou")
            titulo = re.sub(r"\s+", " ", m.group(2)).strip()
            if titulo and INCLUI.search(titulo):
                a = mkato(titulo, link, "INEP")
                if incluir(a):
                    out.append(a)
    return out, ok

def from_mec():
    out, ok = [], 0
    for nome, aid in MEC_ASSUNTOS.items():
        for page in range(1, 5):          # páginas de 40 (recentes->antigos), para ao chegar em <ANO_MIN
            raw = fetch(mec_url(aid, page))
            if not raw:
                break
            try:
                ents = json.loads(raw).get("entidades", [])
            except Exception as e:
                print("  ! mecnormas (%s p%d):" % (nome, page), str(e)[:60])
                break
            ok = 1
            parou = False
            for a in ents:
                titulo = a.get("titulo") or ""
                ementa = a.get("ementa") or ""
                disp, iso = datas(titulo, a.get("dataDePublicacaoString"))
                if iso and int(iso[:4]) < ANO_MIN:
                    parou = True
                    continue
                ato = mkato(titulo, "https://mecnormas.mec.gov.br/pesquisa/detalhar/%s" % a.get("id"),
                            "MEC", ementa, a.get("dataDePublicacaoString"))
                if incluir(ato):
                    out.append(ato)
            if parou or len(ents) < 40:
                break
    return out, ok

def load(p, default):
    if os.path.exists(p):
        try:
            return json.load(io.open(p, encoding="utf-8"))
        except Exception:
            return default
    return default

def main():
    inep, ok1 = from_inep()
    mec, ok2 = from_mec()
    print("Fontes: INEP %d/4 páginas | mecnormas %s" % (ok1, "ok" if ok2 else "FALHOU"))
    if ok1 == 0 and ok2 == 0:
        print("CHECAGEM PARCIAL: nenhuma fonte respondeu nesta rodada.")
        return

    by = {}
    for a in inep + mec:   # INEP primeiro -> prioriza o link do Diário Oficial na deduplicação
        by.setdefault(a["key"], a)
    cur = sorted(by.values(), key=lambda a: a["iso"] or "0000", reverse=True)

    first = not os.path.exists(ATOS)
    prevkeys = set(a.get("key") for a in load(ATOS, []))
    io.open(ATOS, "w", encoding="utf-8").write(json.dumps(cur, ensure_ascii=False, indent=1))
    print("Atos ENADE/PND no total: %d (INEP+MEC, deduplicados)" % len(cur))

    if first:
        print("Baseline criado (primeira execução — nada reportado).")
        return

    novos = [a for a in cur if a["key"] not in prevkeys]
    if not novos:
        print("Sem novidades nesta semana.")
        return

    auto = load(NOVI_AUTO, [])
    ex = set(x.get("link") for x in auto)
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    add = []
    for a in novos:
        if a["link"] in ex:
            continue
        desc = (a["ementa"] + " ") if a["ementa"] else "Ato detectado automaticamente na legislação do INEP/MEC. "
        add.append({"d": a["d"] or hoje, "t": a["titulo"][:140], "x": desc + "(fonte: %s)" % a["fonte"], "link": a["link"]})
    if add:
        io.open(NOVI_AUTO, "w", encoding="utf-8").write(json.dumps(add + auto, ensure_ascii=False, indent=1))
    print("NOVIDADES RELEVANTES: %d" % len(add))
    for a in add:
        print("  -", a["d"], a["t"])

if __name__ == "__main__":
    main()
