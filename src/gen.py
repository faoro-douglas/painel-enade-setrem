# -*- coding: utf-8 -*-
import json, io, os

PORT = json.load(io.open("port.json", encoding="utf-8"))
# normaliza links para o DOU em portugues (sem /en/)
for k in PORT:
    PORT[k]["link"] = PORT[k]["link"].replace("in.gov.br/en/web/dou", "in.gov.br/web/dou")

EDITAIS = {
 "ped": [
  {"n":"Edital nº 49/2026","dt":"24/04/2026 · republicado em 10/08/2026","tit":"ENADE 2026 — edital geral",
   "obj":"Torna públicas as diretrizes, os procedimentos, os prazos e os demais aspectos relativos à realização da edição de 2026 do Enade.",
   "pts":["Edital geral do ENADE 2026: inscrições, questionários, cronograma e regras gerais.",
          "Republicado em 10/08/2026 (motivado pela reforma do Enamed, da Medicina). Para a Pedagogia, manteve as provas e ajustou alguns prazos.",
          "Retificado em 09/09 e 01/10/2026 — detalhes na aba Novidades."],
   "link":"https://www.in.gov.br/web/dou/-/edital-n-49-de-24-de-abril-de-2026-701698729","lb":"Diário Oficial da União (DOU)",
   "retif":[
     {"d":"10/08/2026","t":"Republicação (PDF oficial INEP)","link":"https://download.inep.gov.br/enamed/republicacao_do_Edital_n_49_de_2026.pdf"},
     {"d":"09/09/2026","t":"Retificação (DOU)","link":"https://www.in.gov.br/web/dou/-/edital-730698839"},
     {"d":"01/10/2026","t":"Retificação (DOU)","link":"https://www.in.gov.br/web/dou/-/edital-de-retificacao-735883304"}]},
  {"n":"Edital nº 67/2026","dt":"22/05/2026","tit":"Prova Nacional Docente (PND) 2026",
   "obj":"Torna públicas as diretrizes, os procedimentos, os prazos e os demais aspectos relativos à realização da edição de 2026 da Prova Nacional Docente (PND).",
   "pts":["A prova teórica da Pedagogia (licenciatura) em 2026 É a própria PND — aplicada em 20/09/2026.",
          "Os resultados da licenciatura saem no Sistema PND (pnd.inep.gov.br)."],
   "link":"https://mecnormas.mec.gov.br/pesquisa/detalhar/11604","lb":"Ato oficial (MEC/INEP)",
   "retif":[{"d":"","t":"Retificação do Edital 67 (DOU)","link":"https://www.in.gov.br/web/dou/-/retificacao-728480497"}]},
  {"n":"Edital nº 30/2026","dt":"30/03/2026","tit":"ENADE Licenciaturas — Avaliação da Prática (AP)",
   "obj":"Torna públicas as diretrizes, os procedimentos, os prazos e os demais aspectos relativos à realização da edição de 2026 para os cursos de licenciaturas e da Avaliação da Prática (AP).",
   "pts":["Organiza o ENADE das Licenciaturas em 2026, incluindo a Avaliação da Prática (AP) da Pedagogia.",
          "Define a inscrição e os questionários da AP (orientadores, supervisores e estudantes) e o 2º período da AP."],
   "link":"https://www.in.gov.br/web/dou/-/edital-n-30-de-30-de-marco-de-2026-697037834","lb":"Diário Oficial da União (DOU)",
   "retif":[
     {"d":"","t":"Retificação — Enade das Licenciaturas (DOU)","link":"https://www.in.gov.br/web/dou/-/retificacao-712016305"},
     {"d":"","t":"Retificação — Avaliação da Prática (DOU)","link":"https://www.in.gov.br/web/dou/-/edital-de-retificacao-715670646"}]},
  {"n":"Edital nº 77/2026","dt":"17/06/2026","tit":"AP — convocação de supervisores de estágio",
   "obj":"Convoca os supervisores de estágio curricular supervisionado da Avaliação da Prática (AP) do Enade, das edições de 2024 e 2025, para atualização cadastral no sistema Enade.",
   "pts":["Ato administrativo: atualização cadastral de supervisores de estágio no Sistema Enade."],
   "link":"https://download.inep.gov.br/enade/legislacao/edital_n_77_de_17_de_junho_de_2026.pdf","lb":"PDF oficial (INEP)","retif":[]},
 ],
 "comp": [
  {"n":"Edital nº 49/2026","dt":"24/04/2026 · republicado em 10/08/2026","tit":"ENADE 2026 — edital geral",
   "obj":"Torna públicas as diretrizes, os procedimentos, os prazos e os demais aspectos relativos à realização da edição de 2026 do Enade.",
   "pts":["Edital geral do ENADE 2026: inscrições, questionários, cronograma e regras gerais.",
          "Republicado em 10/08/2026 (motivado pela reforma do Enamed, da Medicina). Para a Engenharia de Computação, manteve a prova (29/11) e ajustou alguns prazos.",
          "Retificado em 09/09 e 01/10/2026 — detalhes na aba Novidades."],
   "link":"https://www.in.gov.br/web/dou/-/edital-n-49-de-24-de-abril-de-2026-701698729","lb":"Diário Oficial da União (DOU)",
   "retif":[
     {"d":"10/08/2026","t":"Republicação (PDF oficial INEP)","link":"https://download.inep.gov.br/enamed/republicacao_do_Edital_n_49_de_2026.pdf"},
     {"d":"09/09/2026","t":"Retificação (DOU)","link":"https://www.in.gov.br/web/dou/-/edital-730698839"},
     {"d":"01/10/2026","t":"Retificação (DOU)","link":"https://www.in.gov.br/web/dou/-/edital-de-retificacao-735883304"}]},
  {"n":"Edital nº 61/2026","dt":"14/05/2026","tit":"ENADE 2026 — bacharelados e tecnológicos",
   "obj":"Torna públicas as diretrizes, os procedimentos, os prazos e os demais aspectos relativos à realização do Enade 2026 para estudantes de cursos de Bacharelado e Superiores de Tecnologia, exceto medicina.",
   "pts":["Aplica-se diretamente à Engenharia de Computação (bacharelado).",
          "Complementa o Edital 49 com os procedimentos específicos dos bacharelados e tecnológicos."],
   "link":"https://www.in.gov.br/web/dou/-/edital-n-61-de-14-de-maio-de-2026-705977430","lb":"Diário Oficial da União (DOU)","retif":[]},
 ],
 "agro": [],
 "enf": [],
 "adm": [],
 "dir": [],
 "psi": [],
}

# novidades: as detectadas pelo robô (novidades_auto.json) vão no topo, seguidas dos marcos fixos (novidades.json)
NOVI = json.load(io.open("novidades.json", encoding="utf-8"))
if os.path.exists("novidades_auto.json"):
    try:
        NOVI = json.load(io.open("novidades_auto.json", encoding="utf-8")) + NOVI
    except Exception:
        pass

ATOS = json.load(io.open("atos.json", encoding="utf-8")) if os.path.exists("atos.json") else []

tpl = io.open("template.html", encoding="utf-8").read()
html = tpl.replace("/*__PORT__*/", json.dumps(PORT, ensure_ascii=False)) \
          .replace("/*__EDITAIS__*/", json.dumps(EDITAIS, ensure_ascii=False)) \
          .replace("/*__NOVI__*/", json.dumps(NOVI, ensure_ascii=False)) \
          .replace("/*__ATOS__*/", json.dumps(ATOS, ensure_ascii=False))
io.open("../index.html", "w", encoding="utf-8", newline="\n").write(html)
print("OK -> ../index.html", len(html), "bytes")
