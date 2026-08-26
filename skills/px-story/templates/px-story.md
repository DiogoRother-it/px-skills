# História: <título>

**ID:** `<PROD>-<FLUXO>-<TELA>` · **Ordem de implementação:** <#> · **Arquivo da UI:** `<caminho>`

**Origem:** `planning/<iniciativa>/requests/<slug>.md` (px-request) · **Data:** <YYYY-MM-DD>

<!-- Uma história = uma tela (ou um modal com lógica própria). Fluxo e público são agrupamento, não recorte. -->
<!-- Teto: até 13 CA e 13 cenários BDD. Acima disso, ou quebra, ou preenche a linha abaixo. -->

**Escopo mantido acima do teto:** <motivo — apagar esta linha se estiver dentro do teto>

## 1. Narrativa
> **Como** <público-alvo do kickoff>, **quero** <ação>, **para** <valor de negócio>.

**Contexto:** <objetivo de negócio, herdado do px-request>

## 2. Critérios de aceite (funcional)
- [ ]
- [ ]
- [ ] (estado empty)
- [ ] (estado error)

## 3. Critérios de usabilidade (rubrica ux-persona)
| Dimensão | Critério | OK? |
|---|---|---|
| Descoberta | | [ ] |
| Clareza | | [ ] |
| Feedback | | [ ] |
| Fricção | | [ ] |
| Sem beco sem saída | | [ ] |
| Fidelidade (UI KIT/design) | | [ ] |
| Autenticidade de dados | | [ ] |

## 4. BDD — cenários (Gherkin, pt-BR)
```gherkin
Funcionalidade: <nome>

  Cenário: <caminho feliz>
    Dado que sou <público-alvo> e estou em <tela/estado>
    Quando <ação pela interface>
    Então <resultado observável>
    E <feedback visível>

  Cenário: <estado vazio>
    Dado <condição de lista/dado vazio>
    Quando <ação>
    Então <mensagem de vazio + próximo passo>

  Cenário: <estado de erro>
    Dado <condição de erro>
    Quando <ação>
    Então <tratamento do erro + como se recuperar>
```

## 5. Rastreabilidade
- **Request de origem:** `planning/<iniciativa>/requests/<slug>.md`
- **Variação de componente:** <item da biblioteca>
- **Público-alvo:** `planning/<projeto>/publico-alvo.md#<público>`
- **UI KIT:** `planning/<projeto>/ui-kit.md`
- **Flow de validação (ux-persona):** `e2e/flows/<id>.md`

## Definition of Ready (trava)
- [ ] Narrativa ancorada num público real
- [ ] Aceite verificável, um por comportamento e por estado
- [ ] Usabilidade por dimensão (N/A justificado onde não se aplica)
- [ ] BDD cobre: feliz + vazio + erro + permissão + regra de negócio
- [ ] Rastreabilidade completa
- **Premissas (respostas "não sei" + default assumido):**
  -

## Próximos passos
- [ ] Gerar flow com `ux-flows`
- [ ] Fechar handoff com `px-handoff` (Definition of Done + sprint + flows) → `px-setup` P4 entrega

<!-- Salvar em: planning/<iniciativa>/stories/<slug>.md -->
