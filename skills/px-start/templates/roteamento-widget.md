# Template — roteador visual do Passo 3 (nível 2.5)

Superfície visual do **Passo 3 (Rotear)** do `px-start`. Apresenta as rotas como
opções clicáveis; o clique devolve a escolha ao chat via `sendPrompt`, exatamente
como o líder UX responderia por texto.

## Quando usar

- **Só** no Passo 3 (a escolha do próximo passo). Não usar nos Passos 0/1.
- **Só se a ferramenta de widget visual (`show_widget`) existir** no ambiente. Se não
  existir, caia no `AskUserQuestion` com as mesmas opções (ver SKILL.md, Passo 3).

## Modelo de informação (a régua)

Cada rota carrega **exatamente 4 informações** — mais que isso é ruído:

1. **Condição na voz do UX** — a frase em que a pessoa se reconhece (não o nome da skill).
2. **Destino** — a skill de destino (`px-intake`/`px-kickoff`/`px-epic`).
3. **Sinal de recomendação** — a diretriz "na dúvida, intake" visível como badge.
4. **Consequência em 1 linha** — o porquê daquela rota.

Abaixo das rotas greenfield, o grupo **"Não é projeto novo?"** reúne as portas de
continuação, com **chip neutro** (cor = idealização; neutro = entrada mecânica):
- **`px-audit`** — produto que já existe e vai ser reformado (redesign).
- **branch + feature** — projeto que já existe e tem identidade, e se quer atacar um
  fluxo/funcionalidade específico: prepara a branch `ux/` a partir da main (via
  `px-setup`) e roteia pra `px-epic` (várias telas) ou `px-request` (uma tela).

São portas à prova de erro caso um caso não-greenfield fure o Passo 0 e caia aqui —
visualmente separadas das rotas de idealização.

A saída **"Meu caso é outro"** é o estado de borda: nunca deixa o UX travado — ela
devolve pro `px-intake` (clarear) e dispara o gate de governança quando for o caso.

## Diretrizes embutidas (não podem sumir na versão visual)

- `px-intake` é o **Recomendado** na dúvida.
- Projeto novo **nunca pula a identidade** (`px-kickoff`) rumo ao `px-request`.

## Como disparar

Chame `show_widget` com o código abaixo. Ele é orientado a dados: para mudar rota ou
diretriz, edite os arrays `chain`/`routes` e a linha `diretriz` — o layout não muda.
Ao receber o `sendPrompt`, o `px-start` segue com o **Eco final** e só então despacha.

```html
<h2 class="sr-only">Roteamento do px-start: escolha guiada do próximo passo, que dispara a decisão de volta ao chat.</h2>
<style>
.px-opt{width:100%;text-align:left;display:flex;gap:12px;align-items:flex-start;background:var(--surface-2);border:0.5px solid var(--border);border-radius:12px;padding:12px 16px;cursor:pointer;margin-bottom:8px}
.px-opt:hover{border-color:var(--border-strong);background:var(--surface-1)}
.px-opt.rec{border:2px solid var(--border-accent)}
.px-chip{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.px-door{width:100%;text-align:left;display:flex;gap:12px;align-items:flex-start;background:var(--surface-1);border:0.5px solid var(--border);border-radius:12px;padding:12px 16px;cursor:pointer;margin-bottom:8px}
.px-door:hover{border-color:var(--border-strong)}
.px-sep{font-size:12px;color:var(--text-muted);margin:16px 0 8px}
.px-esc{width:100%;text-align:left;background:transparent;border:0.5px dashed var(--border);border-radius:12px;padding:10px 16px;cursor:pointer;color:var(--text-secondary);font-size:13px;margin-top:4px}
.px-esc:hover{background:var(--surface-1)}
.px-ico{font-size:16px;line-height:1;display:block;width:16px;height:16px;overflow:hidden;flex-shrink:0}
</style>
<div style="padding:1rem 0">
 <div id="px-focus"></div>
</div>
<script>
const diretriz="Na dúvida, comece por px-intake. Projeto novo nunca pula a identidade (px-kickoff).";
const routes=[
 {i:"ti-help-circle",bg:"--bg-accent",fg:"--text-accent",label:"O problema ainda está vago",porque:"Clareia antes de gastar esforço na identidade.",destino:"px-intake",rec:true,p:"No px-start (Passo 3): meu problema ainda está vago e não sei o tamanho. Seguir para px-intake para clarear antes da identidade."},
 {i:"ti-palette",bg:"--bg-pro",fg:"--text-pro",label:"Quero definir a identidade agora",porque:"Público-alvo + UI KIT, a identidade que todas as telas herdam.",destino:"px-kickoff",rec:false,p:"No px-start (Passo 3): já sei que é um projeto novo e quero definir a identidade agora. Seguir para px-kickoff (público-alvo + UI KIT)."},
 {i:"ti-layout-grid",bg:"--bg-success",fg:"--text-success",label:"Já tenho identidade, é um sistema",porque:"Decompõe o sistema em backlog de telas priorizado.",destino:"px-epic",rec:false,p:"No px-start (Passo 3): já tenho a identidade definida e é um sistema com várias telas. Seguir para px-epic para decompor em backlog."}
];
const doors=[
 {i:"ti-tools",chip:"background:var(--bg-warning);color:var(--text-warning)",dc:"var(--text-warning)",label:"O produto já existe, vou reformar",porque:"Redesign ou aplicar o DS numa base existente.",destino:"px-audit",p:"No px-start (Passo 3): na verdade o produto já existe e vou reformar (redesign). Trocar para a porta brownfield px-audit."},
 {i:"ti-git-branch",chip:"background:transparent;border:0.5px solid var(--border-strong);color:var(--text-secondary)",dc:"var(--text-secondary)",label:"Projeto existe: novo fluxo ou funcionalidade",porque:"Puxa uma branch da main e vai direto pro spec, pulando a identidade.",destino:"px-setup → px-epic / px-request",p:"No px-start (Passo 3): o projeto já existe e tem identidade; quero trabalhar num fluxo/funcionalidade específico. Preparar a branch ux/ a partir da main (via px-setup) e então idealizar: se for várias telas, px-epic; se for uma tela, px-request."}
];
const escape={p:"No px-start (Passo 3): meu caso não é nenhum desses. Me ajude a decidir o caminho certo."};
const focus=document.getElementById("px-focus");
let f='<div style="font-size:12px;color:var(--text-accent);margin-bottom:8px">Você está em px-start · Passo 3</div>'
 +'<div style="font-size:18px;font-weight:500;color:var(--text-primary)">Por onde seguir?</div>'
 +'<div style="font-size:14px;color:var(--text-secondary);line-height:1.6;margin:8px 0 16px">'+diretriz+'</div>';
routes.forEach((r,idx)=>{
 f+='<button class="px-opt'+(r.rec?' rec':'')+'" data-i="'+idx+'">'
  +'<span class="px-chip" style="background:var('+r.bg+');color:var('+r.fg+')"><i class="ti '+r.i+' px-ico" aria-hidden="true"></i></span>'
  +'<span style="flex:1">'
  +'<span style="display:flex;align-items:center;gap:8px"><span style="font-size:14px;font-weight:500;color:var(--text-primary)">'+r.label+'</span>'
  +(r.rec?'<span style="font-size:11px;background:var(--bg-accent);color:var(--text-accent);padding:2px 8px;border-radius:9999px">Recomendado</span>':'')+'</span>'
  +'<span style="display:block;font-size:13px;color:var(--text-secondary);margin-top:2px">'+r.porque+'</span>'
  +'<span style="display:inline-flex;align-items:center;gap:4px;font-size:12px;color:var('+r.fg+');margin-top:6px;font-family:var(--font-mono)">→ '+r.destino+'</span>'
  +'</span></button>';
});
f+='<div class="px-sep">Não é projeto novo?</div>';
doors.forEach((d,idx)=>{
 f+='<button class="px-door" data-door="'+idx+'">'
  +'<span class="px-chip" style="'+d.chip+'"><i class="ti '+d.i+' px-ico" aria-hidden="true"></i></span>'
  +'<span style="flex:1">'
  +'<span style="font-size:14px;font-weight:500;color:var(--text-primary)">'+d.label+'</span>'
  +'<span style="display:block;font-size:13px;color:var(--text-secondary);margin-top:2px">'+d.porque+'</span>'
  +'<span style="display:inline-flex;align-items:center;gap:4px;font-size:12px;color:'+d.dc+';margin-top:6px;font-family:var(--font-mono)">→ '+d.destino+'</span>'
  +'</span></button>';
});
f+='<button class="px-esc" data-esc="1">Meu caso é outro</button>';
focus.innerHTML=f;
focus.addEventListener("click",function(e){
 const dr=e.target.closest("[data-door]");
 if(dr){sendPrompt(doors[+dr.getAttribute("data-door")].p);return}
 if(e.target.closest("[data-esc]")){sendPrompt(escape.p);return}
 const el=e.target.closest("[data-i]");
 if(el)sendPrompt(routes[+el.getAttribute("data-i")].p);
});
</script>
```
