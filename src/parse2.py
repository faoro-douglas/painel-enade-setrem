import subprocess, re, json
META={
 "p161":dict(t="Portaria nº 161/2026 — Específico de Eng. de Computação",q="30 questões de múltipla escolha + 1 discursiva",link="https://www.in.gov.br/web/dou/-/portaria-n-161-de-14-de-abril-de-2026-699947779"),
 "p154":dict(t="Portaria nº 154/2026 — Formação Geral (Bacharelado)",q="15 questões de múltipla escolha",link="https://www.in.gov.br/web/dou/-/portaria-n-154-de-14-de-abril-de-2026-699921720"),
 "p315":dict(t="Portaria nº 315/2025 — Formação Geral Docente",q="30 questões de múltipla escolha + 1 discursiva · comum a todas as licenciaturas",link="https://www.in.gov.br/web/dou/-/portaria-n-315-de-26-de-maio-de-2025-632236512"),
 "p331":dict(t="Portaria nº 331/2025 — Específico de Pedagogia",q="50 questões de múltipla escolha · subsídio: DCN dos cursos de Pedagogia",link="https://www.in.gov.br/web/dou/-/portaria-n-331-de-26-de-maio-de-2025-632239272"),
}
R=["XXIV","XXIII","XXII","XXI","XX","XIX","XVIII","XVII","XVI","XV","XIV","XIII","XII","XI","X","IX","VIII","VII","VI","V","IV","III","II","I"]
RA="(?:"+"|".join(R)+")"
DELIM=r"\s*[-–.]\s"
def load(k):
    s=subprocess.run(["pdftotext","-layout","-enc","UTF-8","pdfs/"+k+".pdf","-"],capture_output=True).stdout.decode("utf-8","replace")
    lines=[l for l in s.split("\n") if not re.search(r"in\.gov\.br|Imprensa Nacional|Semesp|Este conteúdo não substitui|\d{2}/\d{2}/202\d,",l)]
    return re.sub(r"\s+"," "," ".join(lines)).strip()
def clean(x):
    x=x.strip()
    x=re.split(r"\.\s+Art\.\s*\d",x)[0]        # drop any "Art. Nº ..." tail that bled in
    x=x.strip().rstrip(" .;")
    x=re.sub(r"[;,]?\s+e$","",x).strip()        # drop trailing conjunction "e" (only when a real separate word)
    return (x[:1].upper()+x[1:]) if x else x
def between(doc,a,b):
    m=re.search(a+r"(.*?)"+b,doc)
    return m.group(1).strip() if m else ""
def roman_chunks(seg):
    idxs=[(m.start(),m.group(1),m.end()) for m in re.finditer(r"\b("+RA+")"+DELIM, seg)]
    out=[]
    for i,(st,rom,en) in enumerate(idxs):
        nxt=idxs[i+1][0] if i+1<len(idxs) else len(seg)
        out.append((rom, seg[en:nxt].strip()))
    return out
def parse(k):
    doc=load(k)
    perfil=[clean(t) for _,t in roman_chunks(between(doc,r"perfil do[^:]*:",r"\bArt\.\s*\d"))]
    comp_seg=between(doc,r"respectivas\s+habilidades\s*[:.]",r"objetos de conhecimento")
    comp=[]
    for i,(rom,chunk) in enumerate(roman_chunks(comp_seg),1):
        parts=re.split(r"[a-zA-Z]\)\s*[Hh]abilidades\s+vinculadas[^:]*:",chunk,maxsplit=1)
        stmt=re.sub(r"^Compet[êe]ncia\s+"+RA+r"\s*:\s*","",parts[0].strip()).strip().rstrip(".")
        habs=[]
        if len(parts)>1:
            habs=[clean(h) for h in re.split(r"\s\d+\.\s"," "+parts[1]) if h.strip()]
        comp.append({"s":"Competência %s — %s"%(["I","II","III","IV","V"][i-1],stmt),"hab":habs})
    obj_seg=between(doc,r"objetos de conhecimento\s*[:.]",r"\bArt\.\s*\d|entra em vigor|MANUEL")
    obj=[clean(t) for _,t in roman_chunks(obj_seg)]
    m=META[k]
    return dict(t=m["t"],q=m["q"],perfil=perfil,comp=comp,obj=obj,link=m["link"])
PORT={k:parse(k) for k in META}
open("port.json","w",encoding="utf-8").write(json.dumps(PORT,ensure_ascii=False))
for k,v in PORT.items():
    print(k,"| perfil",len(v["perfil"]),"| comp",len(v["comp"]),"hab",[len(c["hab"]) for c in v["comp"]],"| obj",len(v["obj"]))
