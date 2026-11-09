# DS Patterns

> **O que é este arquivo**
> Patterns são estruturas de tela reutilizáveis — blueprints que organizam componentes, informações e fluxos em tipos recorrentes de interface.
> Não são componentes isolados. São modelos de estrutura que resolvem problemas recorrentes de produto.
>
> **Quando consultar**
> Antes de estruturar qualquer tela nova. Sempre verificar: existe um pattern que resolve esse problema? Combinar patterns quando necessário (ex: Listagem + Filtros + CRUD).
>
> **Regra geral**
> Comece pelo pattern existente antes de criar estrutura nova. Novos patterns só são criados quando a mesma estrutura se repetir mais de uma vez no produto e não houver pattern que cubra o caso.
>
> **Hierarquia dos documentos**
> `ds-foundations.md` → tokens, escalas, princípios de base
> `ds-components.md` → specs dos componentes utilizados nos patterns
> `ds-patterns.md` (este) → estruturas de tela
> `uikit-[projeto].html` → implementação visual real do produto

---

## Índice de patterns

- **Página de Listagem** — exibição e gestão de coleções de dados
- **Página de Detalhe** — visualização completa de um registro
- **Formulários** — criação e edição de dados
- **Dashboard** — visão geral com métricas e indicadores
- **Kanban** — gestão visual de itens por status
- **Estados Vazios** — ausência de dados ou primeiro acesso
- **Estados de Erro** — falhas de sistema ou de operação
- **Confirmações** — validação de ações antes de executar
- **Permissões / Acesso Negado** — restrições de acesso
- **Loading State** — estados de carregamento de conteúdo
- **Tabelas com Filtros** — listagem com refinamento de dados
- **CRUD Pattern** — ciclo completo de criação, leitura, edição e exclusão
- **Wizard / Stepper** — fluxos com múltiplas etapas lineares
- **Busca** — localização de dados por termo
- **Filtros** — refinamento de dados por critérios

---

## Página de Listagem

**O que é**
Exibe conjuntos de itens de uma mesma entidade (usuários, contratos, solicitações) de forma estruturada. Permite visualizar, pesquisar, filtrar e executar ações sobre múltiplos registros.

**Quando usar**
Existe coleção de itens da mesma entidade / usuário precisa visualizar dados em massa / há necessidade de busca, filtros ou ordenação / são necessárias ações individuais ou em lote.

**Estrutura base**

```
[ Header da página ]
  Título da entidade
  Ação principal ("Criar novo", "Adicionar item")
  Ações secundárias (quando necessário)

[ Área de busca e filtros ]
  Campo de busca principal
  Filtros rápidos (chips ou toggles)
  Acesso a filtros avançados (Drawer/Modal)

[ Ações em massa ] (quando aplicável)
  Seleção múltipla com checkbox
  Ações: excluir, exportar, alterar status

[ Área de listagem ]
  Tabela estruturada (sistemas administrativos)
  — ou —
  Cards (quando há mais contexto visual por item)

[ Paginação / navegação ]
  Controle de páginas
  — ou —
  Infinite scroll (quando aplicável ao contexto)
```

**Componentes utilizados**
Page Header, Button, Table / Card List, Search Input, Filter Bar / Filter Drawer, Checkbox, Pagination, Empty State, Skeleton (loading), Dropdown Menu (ações por item), Toast.

**Fluxo de interações**
1. Usuário acessa a listagem
2. Sistema carrega dados (loading state)
3. Usuário busca, filtra ou ordena
4. Usuário executa ações individuais ou em massa
5. Sistema atualiza a listagem
6. Usuário navega para detalhe ou cria novo registro

**Variações**
- Listagem simples (sem filtros ou ações em massa)
- Listagem com filtros avançados
- Listagem em tabela (densa, dados estruturados)
- Listagem em cards (mais visual ou contextual)
- Listagem com agrupamento por status/categoria
- Listagem com exportação de dados

**Boas práticas**
- Priorizar clareza na exibição dos dados
- Usar hierarquia visual para diferenciar colunas importantes
- Manter consistência entre listagens do sistema
- Oferecer busca e filtros sempre que houver volume de dados
- Garantir estados bem definidos (loading, empty, error)
- Manter ações principais sempre visíveis e acessíveis

**O que evitar**
- Listagens sem hierarquia clara de informação
- Excesso de colunas sem prioridade
- Filtros complexos sem necessidade
- Ignorar estados vazios ou de erro
- Misturar tabelas e cards sem justificativa de UX

---

## Página de Detalhe

**O que é**
Exibe todas as informações completas de um único item ou registro. Permite visualizar, analisar e executar ações sobre uma entidade específica.

**Quando usar**
Usuário precisa visualizar informações completas de um registro / entidade com múltiplos atributos ou seções / há ações sobre um item específico / usuário navega recorrentemente entre listagem e detalhe.

**Estrutura base**

```
[ Header da página ]
  Nome ou identificador principal do item
  Informações secundárias (status, código, categoria)
  Ações principais (editar, excluir, duplicar)
  Ação de voltar para listagem

[ Área de resumo (overview) ]
  Informações mais importantes do item
  KPIs ou dados-chave (quando aplicável)
  Status visual destacado

[ Seções de conteúdo ]
  Dados gerais
  Informações técnicas
  Histórico / Timeline
  Relacionamentos com outras entidades
  Configurações ou parâmetros

[ Ações contextuais ]
  Ações dentro de seções específicas
  Botões ou menus relacionados ao conteúdo

[ Navegação complementar ] (opcional)
  Tabs (quando há real separação de contexto)
  Breadcrumbs (hierarquia contextual)
```

**Componentes utilizados**
Page Header, Badge/Status, Button, Tabs, Card, Data display (labels, key-value pairs), Table (dados relacionados), Breadcrumb, Modal/Drawer (ações), Empty State, Loading/Skeleton.

**Fluxo de interações**
1. Usuário acessa a partir de uma listagem
2. Sistema carrega os dados (loading state)
3. Usuário visualiza resumo e seções detalhadas
4. Usuário edita, executa ações ou consulta histórico
5. Alterações atualizam a própria página ou redirecionam para formulário

**Variações**
- Detalhe simples (poucas informações)
- Detalhe com abas (conteúdo extenso dividido em tabs)
- Detalhe com histórico completo (timeline/logs)
- Detalhe com dados relacionais (tabelas aninhadas)
- Detalhe read-only (somente visualização, sem ações de edição)

**Boas práticas**
- Priorizar informações mais importantes no topo
- Agrupar conteúdos em seções lógicas
- Usar status e indicadores visuais de forma clara
- Usar tabs apenas com real necessidade de separação de contexto
- Garantir que ações principais estejam sempre acessíveis

**O que evitar**
- Exibir todas as informações sem hierarquia ou agrupamento
- Páginas extremamente longas sem organização por seções
- Ocultar ações principais dentro de menus pouco acessíveis
- Tabs sem necessidade real (fragmentação desnecessária)

---

## Formulários

**O que é**
Pattern para criação e edição de dados. Organiza campos de entrada de forma estruturada, guiando o usuário na inserção de informações de maneira clara, consistente e validada.

**Quando usar**
Criar novos registros / editar informações existentes / coleta estruturada de dados / validação de informações antes de salvar / preenchimento progressivo de dados.

**Estrutura base**

```
[ Header do formulário ]
  Título da ação ("Criar item", "Editar plano")
  Contexto do registro (quando edição)
  Ações principais: Salvar / Cancelar / Salvar e continuar

[ Corpo do formulário ]
  Organizado em seções com título e agrupamento lógico
  Campos ordenados por prioridade e fluxo de preenchimento
  Helper texts próximos aos campos que precisam de contexto

[ Footer com ações ]
  Posicionado de forma sempre acessível (fixo ou no final)
  Hierarquia: Salvar (primário) / Cancelar (secundário)
```

**Componentes utilizados**
Input Text, Textarea, Select, Checkbox, Radio, Switch, Date Picker, Upload, Button, Alert (erros de validação global), Toast (feedback de sucesso).

**Regras de organização**
- Agrupar campos relacionados em seções com título claro
- Campos obrigatórios claramente indicados (asterisco ou label explícito)
- Ordem dos campos deve seguir fluxo natural de preenchimento
- Campos mais importantes e simples primeiro
- Não exigir mais dados do que o necessário

**Validação**
- Mostrar erros próximos ao campo (nunca apenas no topo)
- Mensagem de erro específica: "CPF inválido" e não "campo inválido"
- Validação em tempo real para formatos conhecidos
- Validação ao submeter para regras de negócio
- Alert de resumo de erros quando houver múltiplos campos inválidos

**Variações**
- Formulário em página dedicada (fluxo complexo)
- Formulário em Modal (criação rápida)
- Formulário em Drawer (edição contextual)
- Formulário multi-step (→ Wizard/Stepper)

**Boas práticas**
- Minimizar quantidade de campos
- Usar defaults inteligentes
- Fornecer exemplos no helper text quando o formato não é óbvio
- Manter botão de salvar sempre acessível
- Indicar campos opcionais em vez de obrigatórios quando a maioria é obrigatória

**O que evitar**
- Formulários longos sem agrupamento ou seções
- Labels ambíguos ou placeholders como única instrução
- Validação apenas ao submeter (para formatos de dado)
- Erro genérico no topo sem indicar qual campo

---

## Dashboard

**O que é**
Visão geral do sistema com métricas, indicadores e status relevantes. Permite que o usuário entenda rapidamente o estado do produto sem precisar navegar por diferentes seções.

**Quando usar**
Produto com múltiplos indicadores que precisam de visão consolidada / usuário gestor que monitora status e KPIs / sistema com volume de dados que precisa de sumarização.

**Estrutura base**

```
[ Header ]
  Título do dashboard
  Filtros de período (quando aplicável)
  Ações globais (exportar, atualizar)

[ Área de KPIs / métricas principais ]
  Cards de resumo em grid
  Valores, variações e tendências

[ Área de gráficos / visualizações ]
  Gráficos de série temporal, distribuição ou comparação

[ Área de listagens complementares ]
  Tabelas de itens recentes, alertas ou destaques
```

**Componentes utilizados**
Card de Resumo, Table (básica), Loading/Skeleton, Empty State, Badge, Button, Filter Bar.

**Boas práticas**
- Priorizar as informações mais críticas no topo e à esquerda
- Usar hierarquia visual clara entre KPIs primários e secundários
- Garantir que o dashboard faça sentido mesmo sem interação
- Loading state por bloco, não da tela inteira
- Usar skeleton durante carregamento de cada card/gráfico

**O que evitar**
- Excesso de métricas sem priorização
- Gráficos sem contexto ou título claro
- Dashboard que exige interação para comunicar o essencial
- Poluição visual com muitas informações do mesmo peso

---

## Kanban

**O que é**
Gestão visual de itens organizados em colunas que representam estados ou etapas de um fluxo. Permite mover itens entre estados e entender o fluxo de trabalho de forma visual.

**Quando usar**
Fluxo de trabalho com estados definidos / gestão de tarefas, tickets ou processos / usuário precisa ter visão do volume em cada etapa / movimentação de itens entre estados é recorrente.

**Estrutura base**

```
[ Header do board ]
  Título do board
  Filtros (responsável, período, categoria)
  Ação de criar novo item

[ Colunas de estado ]
  Título da coluna + contador de itens
  Cards dos itens
  Área de drop (drag and drop)
  Ação de criar item na coluna (quando aplicável)

[ Card de item ]
  Título / identificador
  Metadados relevantes (responsável, prazo, prioridade)
  Ações rápidas (opcional)
```

**Componentes utilizados**
Card Interativo, Badge/Tag, Button, Dropdown Menu, Empty State (coluna sem itens), Loading.

**Boas práticas**
- Limitar colunas visíveis (4–6 é o ideal para legibilidade)
- Mostrar contador de itens em cada coluna
- Indicar claramente quando um item está bloqueado ou atrasado
- Drag and drop com feedback visual claro (preview de onde o item cairá)

**O que evitar**
- Excesso de colunas que força scroll horizontal
- Cards com informações demais (deve ser escaneável)
- Falta de feedback durante drag and drop

---

## Estados Vazios

**O que é**
Representa a ausência de dados em uma área do sistema — seja por primeiro acesso, resultado de busca/filtro sem correspondência, ou exclusão de todos os itens.

**Tipos**
- **Primeiro acesso** → usuário ainda não criou nenhum dado
- **Sem resultado** → busca ou filtro não retornou correspondência
- **Sem permissão** → usuário não tem acesso ao conteúdo
- **Erro de carregamento** → dado não pôde ser carregado

**Estrutura base**

```
[ Ícone ou ilustração ]
  Deve ser contextual ao conteúdo ausente

[ Título ]
  Claro e específico ao contexto

[ Descrição ]
  Explica a situação e orienta o próximo passo

[ Ação ] (quando aplicável)
  "Criar primeiro item", "Limpar filtros", "Tentar novamente"
```

**Regras**
- Nunca deixar uma área em branco sem explicação
- Título deve ser específico ao contexto (não "Sem dados")
- Oferecer ação quando houver algo que o usuário possa fazer
- Distinguir "vazio por design" de "erro de carregamento"

**Boas práticas**
- Usar linguagem encorajadora para primeiro acesso
- Para filtro sem resultado: mostrar o que foi buscado e oferecer "Limpar filtros"
- Para erro: explicar o problema e oferecer "Tentar novamente"

---

## Estados de Erro

**O que é**
Comunica falhas de sistema, operação ou acesso de forma clara, orientando o usuário sobre o que aconteceu e o que pode ser feito.

**Tipos**
- **Erro de rede / timeout** → sistema não conseguiu conectar
- **Erro de operação** → ação falhou no processamento
- **Erro 404** → conteúdo não encontrado
- **Erro 500** → falha interna do sistema

**Regras de comunicação**
- Sempre explicar o que aconteceu em linguagem clara
- Oferecer ação de recuperação quando possível ("Tentar novamente", "Voltar")
- Diferenciar erros recuperáveis de erros permanentes
- Não usar jargão técnico para o usuário final (código de erro pode aparecer como informação secundária)

**Estrutura base**

```
[ Ícone de erro ]
[ Título ] — O que aconteceu (claro e direto)
[ Descrição ] — Orientação sobre o próximo passo
[ Ação ] — "Tentar novamente" / "Voltar" / "Falar com suporte"
```

---

## Confirmações

**O que é**
Solicita validação do usuário antes de executar uma ação com consequências significativas — especialmente ações destrutivas ou irreversíveis.

**Quando usar**
- Ação é irreversível (exclusão permanente, cancelamento)
- Ação tem impacto amplo (afetar múltiplos registros)
- Risco de confusão ou erro acidental

**Quando não usar**
- Ações triviais e reversíveis (salvar rascunho, adicionar item)
- Já existe desfazer (undo) disponível
- Excesso de confirmações reduz atenção do usuário

**Estrutura**

```
Dialog de confirmação:
  Título: O que está prestes a acontecer
  Mensagem: Consequência clara da ação
  Ações:
    [Confirmar] → Danger (se destrutivo) / Primary
    [Cancelar] → Secundário
```

**Regras**
- Linguagem objetiva no título: "Excluir projeto" (não "Atenção!")
- Descrever a consequência exata: "Esta ação não poderá ser desfeita"
- Ação de cancelar deve ser o caminho mais fácil (mais à esquerda ou em foco inicial)
- Para ações destrutivas com alto impacto: considerar confirmação por digitação (ex: digitar o nome do item)

---

## Permissões / Acesso Negado

**O que é**
Comunica ao usuário que ele não possui permissão para acessar determinado conteúdo ou executar determinada ação.

**Tipos**
- **Tela inteira bloqueada** → usuário não tem acesso à área
- **Ação bloqueada** → botão ou funcionalidade indisponível para o perfil
- **Conteúdo parcialmente oculto** → parte do conteúdo exige permissão diferente

**Regras**
- Explicar por que o acesso está bloqueado (perfil insuficiente, plano, configuração)
- Oferecer caminho alternativo quando possível ("Solicitar acesso", "Falar com administrador")
- Não mostrar funcionalidade e depois bloquear — ocultar ou desabilitar desde o início
- Distinguir "sem permissão" de "recurso indisponível" (ex: limite de plano)

---

## Loading State

**O que é**
Representa o estado de carregamento de conteúdo, comunicando ao usuário que o sistema está processando ou buscando dados.

**Estratégia por contexto**

| Duração estimada | Componente recomendado |
|---|---|
| < 300ms | Nenhum (carregamento invisível ao usuário) |
| 300ms – 1s | Spinner inline ou Loading compacto |
| > 1s (conteúdo com estrutura conhecida) | Skeleton |
| > 1s (processo com progresso mensurável) | Progress bar |

**Regras**
- Loading por bloco/seção, não da tela inteira — preservar partes já carregadas
- Skeleton deve espelhar o layout real do conteúdo que está sendo carregado
- Nunca usar loading falso (progresso que não reflete o estado real)
- Conteúdo já carregado não deve ser substituído por loading ao interagir

---

## Tabelas com Filtros

**O que é**
Combinação de Table com área de refinamento de dados. Pattern essencial para sistemas com volume alto de registros que precisam de segmentação.

**Estrutura base**

```
[ Barra de busca e filtros ]
  Campo de busca principal (à esquerda)
  Filtros rápidos (chips ou dropdowns inline)
  Acesso a filtros avançados (Drawer)
  Indicação de filtros ativos (chips com remoção individual)
  "Limpar filtros" (quando há filtros ativos)

[ Contagem de resultados ]
  "X resultados" — atualiza conforme filtros aplicados

[ Tabela ]
  Cabeçalho com ordenação por coluna
  Linhas com dados filtrados
  Ações por linha (menu contextual ou inline)

[ Paginação ]
```

**Componentes utilizados**
Search Input, Button, Filter Chip, Drawer (filtros avançados), Table com Interações, Pagination, Badge (contador de filtros ativos), Empty State.

**Regras**
- Filtros rápidos (os mais usados) ficam expostos; filtros avançados vão para Drawer
- Atualizar resultado em tempo real ou com botão "Aplicar" (definir padrão e manter consistente)
- Indicar claramente quantos filtros estão ativos
- Permitir remoção individual de filtros e limpeza total
- Resultados zero devem mostrar o que foi buscado e oferecer "Limpar filtros"

---

## CRUD Pattern

**O que é**
Ciclo completo de **Criar, Ler, Editar e Excluir** registros. Define como as quatro operações se conectam e qual estrutura cada uma usa.

**Mapeamento de operações**

| Operação | Estrutura recomendada |
|---|---|
| **Listar (Read)** | Página de Listagem |
| **Detalhar (Read)** | Página de Detalhe |
| **Criar (Create)** | Modal (rápido) ou Página dedicada (complexo) |
| **Editar (Update)** | Drawer (contextual) ou Página dedicada (complexo) |
| **Excluir (Delete)** | Dialog de confirmação |

**Fluxo padrão**

```
Listagem
  → Criar novo → Modal / Página de formulário
  → Ver detalhe → Página de Detalhe
      → Editar → Drawer / Página de formulário
      → Excluir → Dialog de confirmação
  → Ações em massa → Dialog de confirmação
```

**Regras**
- Criar e editar seguem a mesma estrutura de formulário (campos iguais, layout igual)
- Exclusão sempre com confirmação — nunca desfazível sem alerta
- Após criar/editar: retornar para detalhe ou listagem (definir padrão e manter consistente)
- Feedback de sucesso: Toast após salvar com sucesso

---

## Wizard / Stepper

**O que é**
Fluxo com múltiplas etapas lineares e sequenciais. Divide tarefas complexas em partes menores e gerenciáveis.

**Quando usar**
Processo de configuração com muitos campos / onboarding de novo usuário / fluxo de contratação ou pedido / qualquer jornada em que a ordem das etapas importa.

**Quando não usar**
Formulário simples de 1–2 etapas (usar formulário comum) / etapas não dependem de sequência (→ Tabs).

**Estrutura base**

```
[ Stepper / Indicador de progresso ]
  Etapas numeradas com status (não iniciado / em andamento / concluído)
  Visível durante todo o fluxo

[ Conteúdo da etapa atual ]
  Formulário ou conteúdo da etapa
  Número de campos reduzido (foco no essencial da etapa)

[ Navegação entre etapas ]
  Avançar (primário) — habilita após validação da etapa
  Voltar (secundário)
  Cancelar (terciário ou link)
```

**Regras**
- Cada etapa deve ter objetivo claro e único
- Validar cada etapa antes de avançar — não deixar erro para o final
- Usuário deve poder voltar para etapas anteriores sem perder dados
- Mostrar progresso claro (etapa X de Y)
- Se uma etapa for opcional, indicar explicitamente
- Permitir salvar rascunho em fluxos longos

**Variações**
- Wizard linear (sequência obrigatória)
- Wizard com etapas opcionais
- Wizard com revisão final antes de confirmar

**Boas práticas**
- Não esconder etapas futuras — o usuário deve ver o caminho completo
- Resumo da etapa anterior no topo da próxima (quando relevante)
- Confirmar antes de descartar rascunho ao cancelar

---

## Busca

**O que é**
Permite localizar dados por correspondência de termo. Pode ser integrada a listagens ou funcionar como busca global do sistema.

**Quando usar**
Navegação manual pela lista seria ineficiente / entidades com atributos pesquisáveis / listagem ou estrutura insuficiente para navegação eficiente.

**Estrutura base**

```
[ Campo de busca ]
  Input dedicado, claramente identificável
  Ícone de lupa à esquerda
  Botão de limpar (X) quando há texto

[ Comportamento de pesquisa ]
  Automático (tempo real) — ou — Manual (botão buscar)
  Busca parcial e tolerante a variações

[ Exibição de resultados ]
  Atualização dinâmica da interface
  Highlight dos termos encontrados (quando aplicável)

[ Estado sem resultado ]
  Empty state contextual com o termo buscado
  Orientação sobre como ajustar a busca
```

**Variações**
- Busca simples (texto livre em uma entidade)
- Busca em tempo real (filtro instantâneo)
- Busca avançada (combinada com filtros)
- Busca global (múltiplos módulos)
- Busca com autocomplete / sugestões

**Boas práticas**
- Campo de busca visível e acessível quando é funcionalidade central
- Retornar resultados de forma rápida e previsível
- Suportar busca parcial
- Destacar termos encontrados nos resultados
- Feedback claro quando não houver resultados

**O que evitar**
- Esconder busca em menus ou locais pouco acessíveis
- Exigir termos exatos para encontrar informações
- Ausência de feedback em casos de erro ou sem resultado

---

## Filtros

**O que é**
Refina, segmenta e restringe conjuntos de dados com base em critérios definidos pelo usuário. Complementa a busca para navegação mais precisa.

**Quando usar**
Grande volume de dados com necessidade de segmentação / usuário combina critérios para encontrar informações específicas / múltiplos atributos filtráveis / análise comparativa ou segmentação de dados.

**Estrutura base**

```
[ Área de ativação dos filtros ]
  Filtros rápidos expostos (os mais usados)
  Botão "Filtros avançados" → abre Drawer

[ Filtros rápidos ]
  Chips de seleção direta
  Aplicação imediata

[ Filtros avançados (Drawer) ]
  Conjunto expandido de critérios
  Tipos: Select, Date Picker, Checkbox, Range
  Botões: Aplicar / Limpar

[ Estado de filtros aplicados ]
  Chips com os filtros ativos (com X para remover individualmente)
  "Limpar todos" quando há múltiplos filtros
```

**Variações**
- Filtros simples (rápidos, diretos)
- Filtros avançados (múltiplos critérios em Drawer)
- Filtros persistentes (mantêm estado entre navegações)
- Filtros temporários (resetam ao sair da página)
- Filtros por data (intervalos e períodos)
- Filtros por status ou categorias

**Boas práticas**
- Priorizar filtros mais usados na área principal
- Agrupar filtros de forma lógica e contextual
- Manter clareza sobre quais filtros estão ativos
- Permitir remoção fácil de filtros individuais
- Garantir que filtros e busca funcionem de forma complementar

**O que evitar**
- Misturar todos os filtros diretamente na interface sem organização
- Filtros sem relevância real para o usuário
- Não indicar claramente os filtros ativos
- Comportamentos diferentes de filtro em módulos distintos do sistema
