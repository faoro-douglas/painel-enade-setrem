# Modelo de cronograma ENADE — esqueleto auditado (reutilizar a cada ciclo)

**Para que serve:** a estrutura do cronograma (quais ações existem, quem é responsável, quais são do PI, qual o filtro de cada uma) é **estável a cada ciclo** — só as **datas** mudam de edital para edital. Este arquivo guarda o esqueleto já auditado (28/10/2026, Eng. Computação + Pedagogia) para que, quando um curso entrar em novo ciclo, seja só **preencher as datas do edital** — **nunca refazer a auditoria do zero**.

Formato do painel (em `template.html`, `DATA.<curso>.prazos`): `{d:'texto',s:mk(ano,mês,dia)|null, e:mk(...)|null, t:'título', w:'papéis', de:'descrição'}`.
- `w` define o filtro (função `parseAud`): contém `Procuradoria`/`PI` → PI; `Coordenador` → coord; `Estudante`/`ingressante`/`concluinte` → estudante; `INEP` → Inep. Pode ter vários (`'Procuradoria / Coordenador'`).
- Item **só do PI** → `w:'Procuradoria'` (some para quem não destrava o código).

---

## A. BACHARELADO (e CST) — vale para Agro, Enf (2027), Adm, Dir, Psi (2028), Eng. Comp. (próximos ciclos)
Cronograma = **ANEXO I** (ações comuns, no edital-base do ENADE do ciclo) **+ ANEXO IV** (ações específicas de bacharelado/CST). Onde o edital específico do bacharelado divergir do edital-base republicado, **vale o mais novo (republicação + retificações)**. Modelo pronto hoje: `DATA.comp.prazos` (41 itens) em `template.html` — copiar de lá e trocar as datas.

41 ações (ordem cronológica). Coluna "Fonte da data" = de onde ler a data no novo edital:

| # | Ação | Responsável / `w` | Fonte da data |
|---|------|-------------------|---------------|
| 1 | Enquadramento automático (rótulo Cine Brasil) | INEP | ANEXO I·I |
| 2 | Verificação de informações no Cadastro e-MEC | **PI** + Coord | ANEXO I·II |
| 3 | Verificação do acesso autenticado ao Sistema Enade | **PI** + Coord | ANEXO I·III |
| 4 | Verificação do enquadramento automático | **só PI** | ANEXO I·IV |
| 5 | Registro de declarações de não enquadramento | **só PI** | ANEXO I·V |
| 6 | Inscrição dos concluintes habilitados | Coord | ANEXO I·VI |
| 7 | Acompanhamento das ações dos inscritos (contínuo) | **PI** + Coord | ANEXO I·VIII |
| 8 | Retificação de ações (enquadramento/inscrições concluintes) | **PI** + Coord | ANEXO I·VII |
| 9 | Alteração do município de prova (mobilidade/EaD) | **PI** + Coord | ANEXO IV·II |
| 10 | Preenchimento do cadastro pelo estudante | Estudante | ANEXO IV·I |
| 11 | Questionário do Estudante concluinte (1º e 2º período) | Estudante | ANEXO IV·IV (IV.a/IV.b) |
| 12 | Indicação da área (concluinte c/ +1 inscrição) | Estudante | ANEXO IV·III |
| 13 | Solicitação de atendimento especializado | Estudante | ANEXO IV·V |
| 14 | Solicitação de tratamento pelo nome social | Estudante | ANEXO IV·VI |
| 15 | Resultado do atendimento especializado | INEP | ANEXO IV·VII |
| 16 | Recurso do atendimento especializado | Estudante | ANEXO IV·VIII |
| 17 | Indicação de IES de fronteira (condicional) | **só PI** | ANEXO IV·X |
| 18 | Correção discursiva em espanhol/inglês (IES fronteira) | Estudante | ANEXO IV·XI |
| 19 | Resultado do recurso de atendimento | INEP | ANEXO IV·IX |
| 20 | Inscrição dos ingressantes habilitados | Coord | ANEXO I·IX |
| 21 | Retificação das inscrições de ingressantes | Coord | ANEXO I·X |
| 22 | Questionário do Ingressante | Estudante | ANEXO I·XI |
| 23 | Cartão de Confirmação (locais de prova) | INEP + Estudante | ANEXO IV·XII |
| 24 | Aplicação da prova (horário no edital específico) | INEP + Estud + Coord | ANEXO IV·XIII |
| 25 | Questionário do Coordenador de Curso | Coord | ANEXO I·XII |
| 26 | Declaração de Responsabilidade — inscritos não habilitados | Coord | ANEXO IV·XVII.a |
| 27 | Registro de presença na prova pela IES | Coord | ANEXO IV·XIV |
| 28 | Divulgação de cadernos e gabaritos preliminares | INEP + Estudante | ANEXO IV·XVI |
| 29 | Definição da base de resultados válidos (indicadores) | INEP | ANEXO IV·XV |
| 30 | Divulgação da relação de regulares | INEP + Coord | ANEXO IV·XVII |
| 31 | Declaração de Responsabilidade — demais declarações | Coord | ANEXO IV·XVIII |
| 32 | Dispensa de participação pelo estudante | Estudante | ANEXO IV·XIX |
| 33 | Dispensa de participação pela IES | Coord | ANEXO IV·XX |
| 34 | Análise/deliberação das dispensas pela IES | Coord | ANEXO IV·XXI |
| 35 | Análise, pelo Inep, das dispensas da IES | INEP | ANEXO IV·XXII |
| 36 | Recurso das dispensas do estudante (indef. pela IES) | Estudante | ANEXO IV·XXIII |
| 37 | Recurso das dispensas da IES (indef. pelo Inep) | Coord | ANEXO IV·XXIV |
| 38 | Resultado dos recursos de dispensa | INEP | ANEXO IV·XXV |
| 39 | Gabaritos finais e expectativas de resposta | INEP | ANEXO IV·XXVI |
| 40 | Regularização por ato do Inep | INEP | ANEXO I·XIII |
| 41 | Resultados: Boletim, Microdados, Conceito Enade | INEP + Coord + Estud | ANEXO IV·XXVII |

**Itens do PI no bacharelado (8):** #2,3,4,5,7,8,9,17. Só PI: #4,5,17.

---

## B. LICENCIATURA — vale para Pedagogia (TODO ANO) e qualquer nova licenciatura
Cronograma = **ANEXO I** (comuns) + **ANEXO III** (Licenciaturas/PND, Avaliação Teórica) + **Edital da Avaliação da Prática (AP)** — em 2026 foi o Edital 30, dois períodos. Modelo pronto: `DATA.ped.prazos` (~70 itens) em `template.html`.

- **Bloco comum (ANEXO I):** mesmos itens 1–9, 20–22, 25, 40 do bacharelado (enquadramento, verificações do PI, inscrições, questionário do coordenador, regularização). **Itens do PI na licenciatura (6):** ANEXO I·II, III, IV, V, VII, VIII. Só PI: IV, V. **O ANEXO III e o edital da AP NÃO têm item de PI.**
- **Bloco Avaliação Teórica (ANEXO III):** cadastro/inscrição no Sistema PND, atendimento especializado, nome social, questionário do estudante (1º/2º), prova teórica (= PND), registro de presença, divulgações/recursos de gabarito e discursiva, dispensas, boletim, Conceito Enade. Datas: ANEXO III·I a XXXI.
- **Bloco Avaliação da Prática (AP):** do edital próprio (dois períodos). Atores próprios (supervisor/orientador de estágio) → no painel marco como **Coordenador** (quem opera na IES) com o ator nomeado no título ("AP — ..."). O **Questionário de AP do Estudante** é obrigatório.

---

## C. Checklists (abas PI / Coordenador / Estudante) — estrutura estável
- **PI (bacharelado, 8 + 2 gerais):** acompanhar legislação/prazos · verificar Cadastro e-MEC · verificar acesso ao Sistema Enade · verificar enquadramento (só PI) · registrar não enquadramento (só PI) · retificar ações · alterar município (mobilidade/EaD) · indicar IES de fronteira (só PI) · acompanhar inscritos (contínuo) · acompanhar regularidade/resultados.
- **PI (licenciatura, 6 + 2 gerais):** os mesmos, **sem** "alterar município" e "IES de fronteira".
- **Coordenador:** inscrições/retificação · (licenciatura: Avaliação da Prática) · registro de presença · acompanhar regularidade.
- **Estudante:** questionário do estudante · recursos de gabarito · (licenciatura: Questionário de AP) · dispensa se faltou.

**COMPLETUDE OBRIGATÓRIA (regra, não opção):** cada checklist de papel tem de cobrir **TODA** tarefa daquele papel que está em `prazos[]` (um item pode agrupar vários prazos — ex.: "Dispensas da IES" = solicitar+analisar+recorrer — mas nenhum prazo pode ficar de fora). Itens **só do PI** não entram em coord/estud. As datas do checklist têm de bater com os prazos. **Verificar sempre** (seção F). Já foram esquecidos uma vez: **Questionário do Ingressante** (estudante), **Questionário do Coordenador**, **declarações de responsabilidade**, **dispensas**, **atendimento especializado/nome social**, **cartão de confirmação**. Não repetir.
Modelos prontos: `DATA.comp.pi/coord/estud` e `DATA.ped.pi/coord/estud`.

---

## D. RECEITA para instanciar um curso quando o edital sair (passo a passo)
1. **Confirmar o ciclo** (curso × ano) pela portaria que define as áreas do ENADE (o robô semanal capta; ex. Portaria MEC 276/2026). O ciclo pode mudar — não assumir.
2. **Reunir os editais** do ciclo: o edital-base do ENADE (ANEXO I + o anexo do grau: IV bacharelado / III licenciatura) + o edital específico do grau + (licenciatura) o edital da Avaliação da Prática.
3. **Copiar o esqueleto** do curso-modelo do mesmo grau (`comp` para bacharelado, `ped` para licenciatura) e **trocar só as datas** (`d`, `s`, `e`) pela coluna "Fonte da data" acima. Manter `t`, `w`, `de`. **E reescrever os checklists `pi`/`coord`/`estud` cobrindo TODA tarefa de cada papel** (seção C — completude obrigatória).
4. **Aplicar TODAS as retificações** publicadas no DOU até a data (sempre checar; cada uma pode mudar datas ou desmembrar itens). Vale sempre a **mais nova**.
5. **Conteúdo da prova:** adicionar as **portarias de matriz** do ciclo (Formação Geral + componente específico) em `DATA.<curso>.conteudo`, 100% verbatim (parse2.py/port.json). A prova e as portarias mudam a cada ciclo.
6. **Nota e Conceito:** atualizar históricos/indicadores em `resultados.json` quando os dados oficiais saírem.
7. `DATA.<curso>.wait = false`, ajustar `ano` e `prova`. Rodar `gen.py`, conferir no navegador (sem erro de console), **rodar o pente-fino de completude (seção F)**, rodar o **conferidor** (sessão ENADE 2025, `--previa` e no ar) → só publicar com **PODE PUBLICAR**.

## E. ARMADILHAS já descobertas (não repetir)
- **Republicação vence o edital específico** onde divergem (ex.: indicação da área 12/06 no Ed.61 × 24/06 na republicação → vale 24/06).
- **Conferir os itens do PI na fonte**, não confiar só em resumo — responsável pode vir truncado no PDF.
- **Licenciatura: concluinte é ISENTO da taxa da PND** e inscrito automaticamente (Ed.67/2026 art. 1.5.1). **NÃO** lançar itens de "taxa/isenção/inscrição geral" como tarefa — são de participante externo. Verificar o artigo equivalente no edital do novo ciclo.
- **Excluir itens de outra área** (ex.: gabaritos de Letras Português-Inglês não entram em Pedagogia).
- **Divergência entre editais no mesmo item** (ex.: recurso de dispensa do estudante — coordenador no Anexo III × estudante no Ed.67) → marcar para os **dois papéis** com nota, nunca escolher um e arriscar.
- **IES de fronteira** = condicional (só se a SETREM for designada).
- **NÃO amarrar no status operacional do ano** (ex.: "sem ingressantes em tal curso neste ciclo", "concluintes já inscritos"). Fica ERRADO no ciclo seguinte — quem não teve ingressante este ano pode ter no próximo. Manter SEMPRE a tarefa do edital aparecendo para todos; o painel é reutilizável, não um retrato do ano. (Decisão do Faoro, 30/10/2026 — reverteu a ideia anterior de anotar "sem ingressantes".)
- **Nunca inventar datas antes do edital** — curso sem edital fica `wait:true` ("aguardando publicação"). É isso que mantém o painel confiável.

## F. PENTE-FINO DE COMPLETUDE (rodar sempre antes de publicar um curso novo)
O risco nº 1 é uma aba existir e **não ter tudo** (o coordenador/estudante não vê uma tarefa e perde prazo → "o PI fez errado"). Então, para cada curso não-`wait`:
1. **Cruzamento automático checklist × cronograma** (rodar no navegador, com o painel carregado):
   ```js
   ['ped','comp'].forEach(function(cu){var c=DATA[cu];['pi','coord','estud'].forEach(function(rk){
     var role={pi:'Procuradoria',coord:'Coordenador',estud:'Estudante'}[rk];
     var praz=c.prazos.filter(function(p){return parseAud(p.w).indexOf(role)>=0;}).map(function(p){return p.t;});
     console.log(cu,role,'cronograma:',praz.length,praz,'| checklist:',c[rk].map(function(o){return o.b;}));
   });});
   ```
   Conferir item a item que cada tarefa do cronograma está coberta por algum item do checklist.
2. **Agentes independentes** (pente-fino "caprichado", a pedido do Faoro): 1 agente por dimensão, cobrindo TODAS as abas — (a) checklists pi/coord/estud × cronograma; (b) "O que cai na prova" × portarias/port.json; (c) "Nota e Conceito" + EADs × resultados.json; (d) Editais/Links/Novidades/Legislação + datas × editais. Cada um só lê e reporta lacunas/divergências; eu consolido e corrijo.
3. **Conferidor** (sessão ENADE 2025) `--previa` e no ar → **PODE PUBLICAR**.

## G. COMPORTAMENTOS DE VISÃO E ORDEM (manter sempre — pedidos do Faoro em 28–29/10/2026)
- **Coordenador/estudante NUNCA veem Procuradoria:** itens só-PI ocultos (Calendário e Prazos); itens PI+coord aparecem pra eles só como "Coordenador", sem selo nem a palavra "PI"/"Procuradoria"; descrições sem citar PI. (`visibleToViewer` + `displayAud`, e `de` neutras.)
- **PI destravado:** vê tudo; os itens de Procuradoria vêm **destacados em violeta** (`.pi-focus`) = o que ele precisa fazer; o resto é só acompanhar.
- **Aba Prazos ordenada por status:** primeiro o que está **aberto** (fechando antes no topo), depois o que **vai abrir**, e os **encerrados recolhidos** num `<details>` "Já encerrados" no fim (nunca remover). Mesma lógica do Calendário.
- **Itens sem fim no edital** ("a partir de…" / contínuo): rótulo **"Sem data final"** (não "Em andamento" solto). Não inventar data de término.
- **Legislação** ordena por data no render; retificação cuja data de publicação não vem no título entra no `RET_FIX` do `check_inep.py` (senão o robô volta a datá-la pela data do edital-mãe).
- **Aba "Provas e gabaritos"** (`renderProvas`, tab `pg`): é **automática** — lê a última edição de `RESULTADOS[curso].historico[0].ano` e o `grau`, e linka a página OFICIAL do INEP **por modalidade**: bacharelado → `enade/provas-e-gabaritos`; **licenciatura → `enade-das-licenciaturas/provas-e-gabaritos` + PND (`prova-nacional-docente`)** — NÃO a página geral do ENADE, que é a dos bacharelados (⚠️ erro corrigido em 30/10: a Pedagogia estava apontando pra página dos bacharelados). Vale para os 7 cursos sem retrabalho por ciclo. Decisão do Faoro (30/10): **link oficial**, não PDF embutido nem deep-link direto (que quebram = B.O.). Se o INEP mudar as URLs, trocar as constantes em `renderProvas`. **LIÇÃO (Faoro, 30/10):** conferir que o link leva ao CONTEÚDO certo — renderizar a página e checar, não confiar só em HTTP 200. Vale o mesmo cuidado do pente-fino para QUALQUER feature nova, não só pro cronograma.
- **Próxima avaliação / ciclo (regra do Faoro, 30/10):** só afirmar o ano como FATO se confirmado por **edital/portaria oficial**; o que não der, vai como **"(provável)"**. Hoje: 2026 (comp/ped) confirmado por edital; **2027 (agro/enf) e 2028 (adm/dir/psi) = provável** (editais não publicados). Ciclo trienal (bacharelados) / anual (licenciaturas pela PND) — fonte secundária cita **Portaria MEC 610/2024**, que NÃO confirmei em fonte primária, por isso "provável". A aba Provas deriva o ano da ÚLTIMA prova do `resultados.json` (histórico + conceito pendente no `proximo`), **nunca de memória nem de padrão de ciclo fixo** (os ciclos mudaram com COVID/reforma). Os ciclos podem mudar de novo — o monitor capta os editais.
