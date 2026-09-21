# Modelo de código — `src/onboarding/` (px-tour, alvo App React)

> Modelo, não cópia cega. Os nomes entre `<>` vêm dos artefatos (ID da história, slug do flow,
> rota do request). A anatomia do componente é a de `src/components/ui/onboarding/` (tipos em
> `types.ts`); se este modelo e o `.tsx` divergirem, **o `.tsx` manda** e este arquivo vira débito.
>
> Um passo é escrito **uma vez**, no arquivo da tela, e serve ao tour do fluxo e ao global.
> Permissão filtra em runtime. Nunca escreva passos para um perfil.

## `passos/<tela-slug>.ts` — única fonte de passos da tela

```ts
// Passos de onboarding da tela <Nome> (história <ID-ESTÁVEL>, rota <rota>).
// Fonte: px-tour › tours.md › "<tela-slug>". Não edite a copy aqui sem atualizar o tours.md.
import type { PassoOnboarding } from "@/components/ui/onboarding"

export type Can = (chave: string) => boolean

// Âncoras desta tela. O mesmo id vai no `data-onb` do invólucro visível, na UI.
export const ONB_<TELA> = {
  filtrar: "<id-historia>-filtrar",
  novo: "<id-historia>-novo",
  acoesLinha: "<id-historia>-acoes-linha",
  menuLinha: "<id-historia>-menu-linha",
} as const

const alvo = (id: string) => `[data-onb="${id}"]`

// Cada passo carrega a chave da ação que ensina (<recurso>.<ação>). Sem chave = sempre visível.
export function passos<Tela>(can: Can): PassoOnboarding[] {
  const lista: Array<PassoOnboarding & { permission?: string }> = [
    {
      target: alvo(ONB_<TELA>.filtrar),
      title: "Filtrar a lista",
      content: "Use os filtros para achar um contrato pelo status ou pela unidade.",
      data: { rolar: false },
      // evidência: fricção Descoberta, e2e/reports/<flow>__novice.md #2
    },
    {
      target: alvo(ONB_<TELA>.novo),
      title: "Novo Contrato",
      content: "É aqui que um contrato começa. O botão Novo Contrato abre o formulário.",
      permission: "contratos.gerenciar",
      // evidência: ação principal (B5)
    },
    {
      // Passo de ação: ensina onde clicar. O guia avança sozinho quando o menu surgir.
      target: alvo(ONB_<TELA>.acoesLinha),
      title: "Ações da linha",
      content: "Cada linha tem um menu com as ações do contrato.",
      placement: "left",
      data: { acao: "abrir-menu-linha", avancarQuandoAparecer: alvo(ONB_<TELA>.menuLinha) },
      permission: "contratos.visualizar",
    },
    {
      // Interior do menu: só depois do passo de ação, e esperando o alvo assentar.
      target: alvo(ONB_<TELA>.menuLinha),
      title: "Ver detalhes",
      content: "Ver Detalhes abre a página completa do contrato.",
      data: { aguardarAlvo: true },
      permission: "contratos.visualizar",
    },
  ]
  return lista
    .filter((p) => !p.permission || can(p.permission))
    .map(({ permission: _omit, ...p }) => p)
}
```

## `guias.ts` — registro dos guias

```ts
import { passosContratosLista } from "./passos/contratos-lista"
import { passosContratosNovo } from "./passos/contratos-novo"
import { passosContratosDetalhe } from "./passos/contratos-detalhe"
import type { Can } from "./passos/contratos-lista"

export const PRODUTO = "<produto>"

// Uma tela, uma função de passos. A chave é o slug da tela usado em useGuiaDaTela.
export const PASSOS = {
  "contratos-lista": passosContratosLista,
  "contratos-novo": passosContratosNovo,
  "contratos-detalhe": passosContratosDetalhe,
} satisfies Record<string, (can: Can) => unknown>

export type Tela = keyof typeof PASSOS

// Um flow do ux-flows, um guia. `telas` na ordem em que o público as percorre.
export const FLUXOS = {
  "novo-contrato": { id: `${PRODUTO}-novo-contrato`, telas: ["contratos-lista", "contratos-novo"] as Tela[] },
  "ver-contrato": { id: `${PRODUTO}-ver-contrato`, telas: ["contratos-lista", "contratos-detalhe"] as Tela[] },
} as const

// Global: fluxos na ordem da jornada do público (px-epic B2). Tela repetida entra uma vez.
export const GLOBAL = { id: `${PRODUTO}-global`, fluxos: ["novo-contrato", "ver-contrato"] as const }

// Subir a versão do guia sempre que os passos mudarem: reexibe uma vez a quem já viu.
export const VERSAO: Record<string, number> = {
  [FLUXOS["novo-contrato"].id]: 1,
  [FLUXOS["ver-contrato"].id]: 1,
  [GLOBAL.id]: 1,
}

export const PISO_PASSOS_FLUXO = 3

export function telasDoGlobal(): Tela[] {
  const vistas = new Set<Tela>()
  for (const f of GLOBAL.fluxos) for (const t of FLUXOS[f].telas) vistas.add(t)
  return [...vistas]
}
```

## `use-guia-da-tela.ts` — resolve a jornada e monta o `useOnboarding`

```ts
import { useOnboarding, consumirContinuacaoOnboarding } from "@/components/ui/onboarding"
import type { EventoOnboarding } from "@/components/ui/onboarding"
import { FLUXOS, GLOBAL, PASSOS, PISO_PASSOS_FLUXO, VERSAO, telasDoGlobal, type Tela } from "./guias"
import type { Can } from "./passos/contratos-lista"

// INTEGRATION BOUNDARY: autorização real do produto. Hoje mock permissivo.
// MOCK:
const canMock: Can = () => true

// INTEGRATION BOUNDARY: telemetria e resposta da pesquisa de satisfação.
function onEvento(e: EventoOnboarding) {
  console.info("[onboarding]", e)
}

const total = (telas: Tela[], can: Can) => telas.reduce((n, t) => n + PASSOS[t](can).length, 0)

function fluxosDaTela(tela: Tela) {
  return Object.values(FLUXOS).filter((f) => f.telas.includes(tela))
}

/**
 * Regras:
 * 1. Jornada em curso vence: global primeiro, depois o fluxo que contém a tela.
 *    `consumirContinuacaoOnboarding` só devolve (e apaga) a marca do guia pedido.
 * 2. Sem jornada em curso, a tela abre o guia do fluxo do qual ela é a PRIMEIRA tela.
 *    Tela que não abre fluxo nenhum: passos vazios (só participa quando uma jornada chega nela).
 * 3. Piso: fluxo com menos de PISO_PASSOS_FLUXO passos após o filtro fica sem gatilho
 *    (passos vazios desligam chamariz e disparo automático). Os passos seguem no global.
 */
export function useGuiaDaTela(tela: Tela, opts?: { can?: Can; autoIniciar?: boolean; csat?: boolean }) {
  const can = opts?.can ?? canMock
  const passosDaTela = PASSOS[tela](can)

  const continuacao =
    consumirContinuacaoOnboarding(GLOBAL.id) ??
    fluxosDaTela(tela).map((f) => consumirContinuacaoOnboarding(f.id)).find(Boolean) ??
    null

  const fluxoQueAbreAqui = Object.values(FLUXOS).find((f) => f.telas[0] === tela)

  let id: string
  let passos = passosDaTela
  let jornada

  if (continuacao) {
    id = continuacao.guia
    jornada = { ...continuacao, emCurso: true }
  } else if (fluxoQueAbreAqui) {
    id = fluxoQueAbreAqui.id
    const totalFluxo = total(fluxoQueAbreAqui.telas, can)
    if (totalFluxo < PISO_PASSOS_FLUXO) passos = []
    jornada = { total: totalFluxo }
  } else {
    id = `${tela}-avulso`
    passos = []
    jornada = undefined
  }

  const controle = useOnboarding({
    id,
    versao: VERSAO[id] ?? 1,
    passos,
    jornada,
    autoIniciar: opts?.autoIniciar ?? true,
    csat: { ativo: opts?.csat ?? true },
    onEvento,
  })

  return { controle, id, deslocamentoAtual: (jornada?.deslocamento ?? 0), totalJornada: jornada?.total ?? passos.length }
}

// Usado pelo gatilho do global, no shell.
export function totalDoGlobal(can: Can = canMock) {
  return total(telasDoGlobal(), can)
}
```

## `continuacao.ts` — bastão entre telas

```ts
import { marcarContinuacaoOnboarding } from "@/components/ui/onboarding"
import type { ControleOnboarding } from "@/components/ui/onboarding"

/**
 * Chame no handler que navega (ex.: "Ver Detalhes" da linha) ANTES de trocar de rota.
 * Só marca se o guia está rodando e o passo atual é o último desta tela: é o passo de
 * ação que atravessa telas. O destino consome em useGuiaDaTela e entra direto no passo a
 * passo, sem repetir o modal, com o contador continuando.
 */
export function marcarContinuacaoSeAtivo(
  controle: ControleOnboarding,
  totalJornada: number,
  deslocamentoAtual: number,
) {
  if (!controle.ativo) return
  const ultimoDaTela = controle.indicePasso === controle.passos.length - 1
  if (!ultimoDaTela) return
  marcarContinuacaoOnboarding({
    guia: controle.id,
    deslocamento: deslocamentoAtual + controle.passos.length,
    total: totalJornada,
  })
}
```

## Fiação na tela (as três pontas)

```tsx
// Tela <Nome>: só a fiação do onboarding. O resto da tela não muda.
import { Onboarding } from "@/components/ui/onboarding"
import { useGuiaDaTela } from "@/onboarding/use-guia-da-tela"
import { marcarContinuacaoSeAtivo } from "@/onboarding/continuacao"
import { ONB_<TELA> } from "@/onboarding/passos/<tela-slug>"

export function Tela<Nome>({ can, navigate }: Props) {
  const { controle, totalJornada, deslocamentoAtual } = useGuiaDaTela("<tela-slug>", { can })

  // Gaveta desta tela: não fechar enquanto o guia está rodando; devolver o estado ao concluir.
  const [gavetaAberta, setGavetaAberta] = useState(false)
  const fecharGaveta = () => { if (!controle.ativo) setGavetaAberta(false) }

  return (
    <>
      <header className="flex items-center gap-2">
        <h1>Contratos</h1>
        {/* Ajuda só na PRIMEIRA tela de cada fluxo. */}
        <Onboarding.Ajuda controle={controle} dica="Guia de Contratos" />
      </header>

      {/* Âncora no invólucro visível, do tamanho do controle. */}
      <div data-onb={ONB_<TELA>.filtrar} className="w-full max-w-xs">
        <Input ... />
      </div>
      <Button data-onb={ONB_<TELA>.novo}>Novo Contrato</Button>

      <DropdownMenuTrigger data-onb={ONB_<TELA>.acoesLinha} />
      <DropdownMenuContent data-onb={ONB_<TELA>.menuLinha}>
        <DropdownMenuItem
          onSelect={() => {
            marcarContinuacaoSeAtivo(controle, totalJornada, deslocamentoAtual)
            navigate("/contratos/123")
          }}
        >
          Ver Detalhes
        </DropdownMenuItem>
      </DropdownMenuContent>

      <Onboarding.Intro
        controle={controle}
        titulo="Contratos"
        descricao="Aqui você cria contratos e acompanha cada etapa até a assinatura."
      >
        <Onboarding.Intro.Topicos>
          <li>Filtrar e achar um contrato</li>
          <li>Criar um contrato novo</li>
          <li>Abrir os detalhes de um contrato</li>
        </Onboarding.Intro.Topicos>
      </Onboarding.Intro>
      <Onboarding controle={controle} />
    </>
  )
}
```

## `gatilho-global.tsx` — no menu de ajuda do shell

```tsx
// Divergência declarada do DS: a spec põe a bússola ao lado do título da seção; o global
// não tem seção, então o gatilho vive no menu de ajuda do shell (tours.md › Divergências).
import { Onboarding, marcarContinuacaoOnboarding } from "@/components/ui/onboarding"
import { FLUXOS, GLOBAL } from "./guias"
import { totalDoGlobal } from "./use-guia-da-tela"

export function GatilhoGlobal({ navigate, can }: { navigate: (rota: string) => void; can?: Can }) {
  const primeiroFluxo = FLUXOS[GLOBAL.fluxos[0]]
  const rotaInicial = "<rota da primeira tela do primeiro fluxo>"
  return (
    <DropdownMenuItem
      onSelect={() => {
        // Deixa o bastão do global antes de ir para a primeira tela; lá o useGuiaDaTela
        // consome e abre o modal do global (emCurso false: é o início da jornada).
        marcarContinuacaoOnboarding({ guia: GLOBAL.id, deslocamento: 0, total: totalDoGlobal(can) })
        navigate(rotaInicial)
      }}
    >
      Tour Guiado do Produto
    </DropdownMenuItem>
  )
}
```

> Atenção: `consumirContinuacaoOnboarding` no destino devolve `emCurso` implícito só se você o
> passar. Para o **início** do global, o destino deve abrir o modal (porta única): trate
> `deslocamento === 0` como início e monte `jornada: { total }` sem `emCurso`.

## `e2e/tours/<fluxo-slug>.spec.ts` — o tour percorrido de ponta a ponta

```ts
import { test, expect } from "@playwright/test"

test("tour <fluxo-slug> percorre todos os passos", async ({ page }) => {
  await page.goto("<rota da primeira tela>")
  await page.getByRole("button", { name: "Guia de Contratos" }).click()
  await page.getByRole("button", { name: "Iniciar Tour Guiado" }).click()
  // Passo 1
  await expect(page.locator("[data-onboarding-passo]")).toHaveAttribute("data-onboarding-passo", "0")
  await page.getByRole("button", { name: "Próximo" }).click()
  // Passo de ação: clicar no destaque
  await page.locator('[data-onb="<id-historia>-acoes-linha"]').click()
  // Continuação para a próxima tela
  await page.getByRole("menuitem", { name: "Ver Detalhes" }).click()
  await expect(page).toHaveURL(/contratos\/\d+/)
  await expect(page.locator("[data-slot=onboarding-contador]")).toContainText("Passo 4 de")
  // ... até Finalizar
  await page.getByRole("button", { name: "Finalizar" }).click()
  await expect(page.getByText("Como foi este guia para você?")).toBeVisible()
})
```
