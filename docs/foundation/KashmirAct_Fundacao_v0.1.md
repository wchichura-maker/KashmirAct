# KASHMIRACT — DOCUMENTO DE FUNDAÇÃO
## Versão 0.1 — Visão, objetivos, arquitetura e mecânicas fundamentais

**Status:** Fundação conceitual  
**Projeto:** KashmirAct  
**Relação com o projeto anterior:** projeto novo e independente; o Kashmir original permanece preservado  
**Referência criativa principal:** experiência de progressão e criação de *Overgeared*, reinterpretada como jogo não-VR  
**Engine:** candidata; Godot 4.6 é a base inicial de prototipagem, não uma decisão irreversível

---

# 1. Declaração de identidade

KashmirAct será um RPG de ação 3D, não-VR, centrado em uma ideia:

> **O jogador não escolhe simplesmente uma classe. Ele constrói, através da forma como joga, o personagem que se torna.**

A experiência pretendida é inspirada na fantasia de *Overgeared*: descoberta, criação, maestria, equipamentos autorais, profissões, habilidades próprias, reputação e evolução extraordinária.

Não será uma adaptação literal do manhwa, nem uma tentativa de reproduzir sua propriedade intelectual. O objetivo é reproduzir a **estrutura de fantasia de poder e autoria do jogador** através de sistemas próprios.

O segundo princípio é:

> **Itens, habilidades e estilos de combate devem ser resultados de sistemas, não apenas conteúdo previamente escrito pelos designers.**

---

# 2. Objetivo máximo

Construir um mundo RPG em que:

1. o jogador possa desenvolver um estilo de combate próprio;
2. a forma de jogar altere progressivamente a identidade mecânica do personagem;
3. profissões permitam criar, projetar, aperfeiçoar e transformar equipamentos;
4. itens tenham autoria, histórico, qualidade, composição, propriedades e evolução;
5. habilidades sejam compostas por módulos e possam surgir de experimentação;
6. o sistema de IA observe o comportamento do jogador e procure possibilidades novas;
7. diferentes jogadores possam começar semelhantes e terminar com personagens mecanicamente muito diferentes;
8. o mundo reconheça e reaja à reputação e às criações do jogador;
9. o sistema continue produzindo combinações válidas sem depender de milhares de objetos feitos manualmente;
10. todas as liberdades do jogador sejam limitadas por regras sistêmicas verificáveis, nunca por arbitrariedade textual.

---

# 3. Fantasia central do jogador

O jogador deve sentir:

> “Esse personagem existe porque eu joguei desse jeito.”

E também:

> “Esse equipamento é meu porque eu o projetei, construí e aperfeiçoei.”

E:

> “Essa técnica é minha porque surgiu da forma como combino meus movimentos, arma, recursos e timing.”

E finalmente:

> “Outro jogador não precisa ter o mesmo personagem que eu.”

---

# 4. Gênero-alvo

## Classificação principal

**3D Real-Time Action RPG / Sandbox Progression RPG**

## Subgêneros e influências sistêmicas

- Action RPG
- RPG de progressão
- Sandbox sistêmico
- Crafting RPG
- Character-building RPG
- Adventure RPG
- Social/world simulation
- Emergent gameplay

Não será inicialmente definido como MMORPG. A arquitetura deve permitir multiplayer futuramente, mas o primeiro objetivo é provar a experiência de combate, criação e progressão em single-player.

---

# 5. Câmera e controle

A direção inicial será:

**Third Person 3D**

A câmera deve permitir liberdade suficiente para observar:

- personagem;
- arma;
- postura;
- alvo;
- terreno;
- impactos;
- habilidades;
- equipamentos.

A câmera não deve esconder a autoria corporal do jogador.

## Controle corporal

O personagem possuirá uma hierarquia de controle:

### Locomoção
- caminhar;
- correr;
- sprint;
- acelerar;
- desacelerar;
- saltar;
- agachar;
- esquivar;
- rolar;
- mudar direção.

### Orientação
- direção do corpo;
- direção da cabeça;
- direção da câmera;
- direção da arma;
- direção de ataque.

### Postura
- neutra;
- ofensiva;
- defensiva;
- baixa;
- alta;
- contextual.

### Membros e equipamento
- mão esquerda;
- mão direita;
- armas;
- escudo;
- ferramentas;
- objetos carregados.

O objetivo não é controlar literalmente cada osso. O objetivo é permitir controle suficientemente granular para que ações diferentes produzam resultados visual e mecanicamente diferentes.

---

# 6. Modelo de combate

O combate será em tempo real.

Não haverá dependência de uma grade de turnos ou de uma lista fixa de habilidades pré-determinadas.

## Unidade fundamental

Uma ação de combate é composta por:

**intenção + movimento + postura + direção + arma + timing + estado + contexto**

Exemplo:

```text
Dodge Left
→ Rotate 90°
→ Low Stance
→ Rising Slash
→ Fire Infusion
→ Recovery
```

Isso representa uma técnica possível.

Outra sequência poderá produzir um resultado completamente diferente.

---

# 7. Sistema de Motion Primitives

O combate será construído a partir de unidades reutilizáveis de movimento.

Exemplos:

- Step
- Dash
- Backstep
- Dodge
- Turn
- Rotate
- Crouch
- Jump
- Lunge
- Swing
- Thrust
- Raise
- Lower
- Guard
- Parry
- Recover
- Charge

Essas primitivas não são habilidades finais.

São componentes.

O sistema pode combiná-las em técnicas.

---

# 8. Sistema de habilidades

Uma habilidade será tratada como uma composição de fases e eventos.

Modelo conceitual:

```text
TRIGGER
  ↓
PREPARATION
  ↓
MOVEMENT
  ↓
WEAPON / CAST
  ↓
EFFECT
  ↓
IMPACT
  ↓
SECONDARY EFFECTS
  ↓
RECOVERY
```

Cada estágio poderá possuir condições.

Exemplo:

```text
Trigger:
Attack while Fire Affinity > threshold

Movement:
Forward Lunge

Weapon:
Two-handed Slash

Effect:
Fire Trail

Impact:
Physical + Fire

Secondary:
Burn

Recovery:
0.8s
```

---

# 9. Skill Composer

O jogo terá uma camada de composição de habilidades.

O jogador poderá, de forma progressiva, modificar:

- sequência;
- direção;
- tipo de movimento;
- arma;
- elemento;
- alcance;
- área;
- força;
- custo;
- risco;
- recuperação;
- condições de ativação;
- efeitos secundários.

A liberdade será limitada pelo **Rule Validator**.

Uma habilidade só existe no jogo se:

1. seus componentes forem válidos;
2. seus custos forem calculáveis;
3. seu comportamento puder ser executado pelo runtime;
4. sua combinação não violar regras fundamentais;
5. seus parâmetros estiverem dentro dos limites sistêmicos.

---

# 10. Descoberta de habilidades

O jogador não receberá necessariamente todas as técnicas através de uma árvore.

O sistema poderá reconhecer padrões de utilização.

Exemplo:

```text
Dodge Left
+
Rotation
+
Rising Slash
```

Se o jogador executar essa sequência repetidamente, o sistema pode registrar:

**Padrão emergente detectado.**

Depois poderá surgir:

**Nova possibilidade de técnica.**

A técnica só será considerada aprendida quando o sistema de progressão permitir.

---

# 11. Agente de descoberta de combate

Um sistema especializado de IA/algoritmo analisará o histórico de combate.

### Funções

```text
observe_player()
record_telemetry()
analyze_style()
extract_patterns()
generate_candidates()
simulate_candidates()
score_candidates()
validate_candidate()
propose_discovery()
record_discovery()
```

## Objetivo

Não procurar todas as combinações possíveis.

Procurar **adjacências relevantes ao estilo do jogador**.

Exemplo:

Se o jogador usa constantemente:

```text
Dodge → Slash
```

o agente pode experimentar:

```text
Dodge → Rotate → Slash
Dodge → Element → Slash
Dodge → Parry → Slash
Dodge → Jump → Slash
```

O sistema deve explorar primeiro as regiões do espaço de possibilidades que tenham maior relação com o comportamento observado.

---

# 12. Simulação de candidatos

Antes de transformar uma descoberta em conteúdo persistente, o sistema poderá testar a combinação em ambiente de simulação.

Parâmetros possíveis:

- dano;
- duração;
- custo;
- alcance;
- consumo de stamina;
- recuperação;
- risco;
- chance de acerto;
- interrupção;
- mobilidade;
- crowd control;
- eficiência contextual.

O simulador deve ser determinístico sempre que possível.

A simulação deve poder rodar sem apresentação gráfica, permitindo milhares de testes baratos.

---

# 13. Progressão do personagem

Não haverá uma dependência obrigatória de classes rígidas.

O personagem será definido por várias dimensões:

```text
PLAYER
├── ATTRIBUTES
├── COMBAT STYLE
├── WEAPON MASTERY
├── PROFESSION MASTERY
├── SKILL DISCOVERY
├── ITEM RELATION
├── KNOWLEDGE
├── REPUTATION
└── SOCIAL HISTORY
```

A identidade mecânica surge da combinação.

---

# 14. Classes e arquétipos

O conceito de “classe” será reinterpretado.

A classe pode ser:

1. escolhida parcialmente;
2. descoberta;
3. construída;
4. reconhecida pelo mundo;
5. evoluída pelo comportamento.

Exemplo:

Um jogador especializado em:

- espada;
- fogo;
- mobilidade;
- parry;
- crafting de armas;

poderá desenvolver um arquétipo compatível com esse padrão.

Outro jogador, usando a mesma arma inicial, poderá desenvolver um arquétipo completamente diferente.

---

# 15. Behavioral Character Development

O jogo deverá registrar como o personagem joga.

Variáveis de longo prazo podem incluir:

- preferência de distância;
- agressividade;
- uso de defesa;
- mobilidade;
- frequência de esquiva;
- preferência de armas;
- utilização de magia;
- uso de crafting;
- exploração;
- comércio;
- suporte a aliados;
- comportamento social;
- risco;
- repetição de técnicas.

Esses dados não devem apenas produzir estatísticas de analytics. Eles devem alimentar mecânicas.

---

# 16. Profissões

Profissões serão sistemas de gameplay, não apenas menus de receitas.

Exemplos iniciais:

- Blacksmith
- Armorsmith
- Weaponsmith
- Tailor
- Leatherworker
- Alchemist
- Enchanter
- Jewelcrafter
- Carpenter
- Engineer
- Cook
- Scribe
- Miner
- Hunter
- Tinker

A profissão determina **o que o jogador consegue manipular e compreender**, e não simplesmente uma lista fixa de itens.

---

# 17. Criação de equipamentos

A criação de itens deve permitir decisões sobre:

### Estrutura
- tipo;
- forma;
- proporção;
- tamanho;
- peso;
- equilíbrio;
- partes.

### Material
- metal;
- madeira;
- couro;
- tecido;
- mineral;
- cristal;
- material mágico;
- materiais raros.

### Processo
- fundição;
- forjamento;
- têmpera;
- corte;
- montagem;
- polimento;
- encantamento;
- costura;
- infusão;
- combinação.

### Propriedades
- dano;
- defesa;
- alcance;
- velocidade;
- durabilidade;
- afinidade;
- propriedades elementais;
- efeitos especiais.

---

# 18. Item Graph

Cada item deverá possuir um histórico estrutural.

Exemplo:

```text
ITEM
├── DESIGN
├── MATERIALS
├── MANUFACTURING
├── QUALITY
├── MODIFIERS
├── CREATOR
├── CREATION_DATE
├── USAGE_HISTORY
├── REPAIR_HISTORY
├── UPGRADE_HISTORY
└── UNIQUE_ID
```

Dessa forma, dois itens visualmente semelhantes ainda podem ser mecanicamente diferentes.

---

# 19. Autoria

O criador deve ser parte do item.

Itens especiais podem carregar:

- nome do criador;
- profissão do criador;
- método de fabricação;
- qualidade;
- reputação;
- número de versões;
- histórico;
- proprietários anteriores.

A autoria pode ter impacto no mundo.

NPCs podem reconhecer artesãos famosos.

Mercadores podem pagar mais por determinados criadores.

Guildas podem procurar determinados especialistas.

---

# 20. Blueprint / Design System

A profissão não deve permitir criar qualquer resultado sem conhecimento.

O jogador pode possuir:

- conhecimento;
- blueprint;
- técnica;
- fórmula;
- material;
- ferramentas;
- experiência.

Um blueprint define uma **possibilidade**, não necessariamente um resultado fixo.

Isso permite que o mesmo projeto tenha resultados diferentes conforme:

- matéria-prima;
- habilidade;
- processo;
- qualidade;
- profissional;
- ferramenta;
- execução.

---

# 21. Crafting manual

Sempre que possível, operações críticas de fabricação terão componente interativo.

A qualidade poderá depender de:

- timing;
- sequência;
- preparação;
- temperatura;
- escolha de material;
- ferramenta;
- experiência.

Isso não deve virar um minigame repetitivo obrigatório para cada item trivial.

O nível de interação deve acompanhar a importância da criação.

---

# 22. Qualidade de item

Os itens devem possuir propriedades mensuráveis.

Exemplo:

```text
Durability
Sharpness
Balance
Density
Integrity
Magic Conductivity
Material Purity
Craftsmanship
```

A qualidade final deriva desses parâmetros.

O sistema não deve simplesmente sortear “épico”.

A classificação deve ser consequência das propriedades.

---

# 23. Evolução de itens

Itens podem mudar com:

- uso;
- reparo;
- upgrade;
- alteração;
- combinação;
- exposição a materiais;
- eventos;
- magia;
- experiência do usuário.

Uma arma pode se tornar especial pela história acumulada.

---

# 24. Itens e habilidades devem conversar

Um equipamento não é somente um conjunto de atributos.

Ele pode modificar:

- movimentos;
- alcance;
- sequência;
- custo;
- efeitos;
- possibilidades de habilidades;
- regras de interação.

Exemplo:

Uma espada muito flexível pode permitir um tipo de golpe que uma espada rígida não permite.

---

# 25. Física como componente do sistema

A física não deve controlar absolutamente tudo.

Ela será usada onde contribuir para:

- impacto;
- deslocamento;
- colisão;
- ragdoll parcial;
- objetos físicos;
- interação;
- destruição contextual;
- animação secundária.

A regra de dano continuará sendo determinística e controlável.

---

# 26. Animação

A animação será híbrida:

**Authoritative animation + procedural modification.**

Camadas previstas:

```text
BASE LOCOMOTION
      ↓
MOTION SELECTION
      ↓
COMBAT ANIMATION
      ↓
PROCEDURAL IK
      ↓
WEAPON / HAND ALIGNMENT
      ↓
SECONDARY MOTION
      ↓
PHYSICAL RESPONSE
```

O objetivo é evitar tanto:

- animações rígidas demais;

quanto:

- física sem controle artístico.

---

# 27. Requisitos técnicos do sistema corporal

O personagem precisa suportar:

- IK;
- constraints;
- mão aderindo à arma;
- pés adaptados ao terreno;
- cabeça mirando alvos;
- ajuste do tronco;
- braços orientados por alvo;
- animação aditiva;
- blending;
- motion matching ou sistema equivalente;
- partial-body animation;
- physical animation;
- ragdoll parcial.

---

# 28. Mundo

O mundo deve ser sistêmico.

NPCs, profissões, economia, facções e mercado precisam reconhecer que jogadores criam coisas.

A existência de uma criação excepcional deve ter consequências.

---

# 29. NPCs

NPCs devem possuir:

- identidade persistente;
- profissão;
- conhecimento;
- relações;
- reputação do jogador;
- memória;
- preferências;
- objetivos;
- disponibilidade.

Um personagem que fique famoso como ferreiro não deverá ser percebido como um aventureiro genérico.

---

# 30. Mercado

O mercado deverá aceitar itens criados pelo jogador.

Preço pode depender de:

- qualidade;
- material;
- raridade;
- reputação;
- demanda;
- identidade do criador;
- histórico;
- eficácia;
- aparência;
- disponibilidade.

---

# 31. Reputação

Reputação não é apenas um número.

Deve existir por:

- região;
- profissão;
- guilda;
- facção;
- classe social;
- tipo de atividade.

Uma pessoa pode ser:

- desconhecida em uma cidade;
- famosa entre ferreiros;
- procurada por uma guilda militar;
- odiada por uma facção.

---

# 32. IA do jogo

A IA do projeto será dividida em camadas.

### Runtime AI

Responsável por NPCs e inimigos.

### Analysis AI

Responsável por compreender comportamento do jogador.

### Discovery Agent

Responsável por experimentar combinações.

### Content AI

Responsável por linguagem, descrição, naming e suporte criativo.

### Development AI

Responsável por ajudar o time de desenvolvimento através do Kashmir AI Studio.

Essas camadas não devem ter a mesma autoridade.

---

# 33. Regra fundamental da IA

A IA poderá:

- observar;
- analisar;
- sugerir;
- simular;
- gerar candidatos;
- descrever.

A IA não poderá quebrar diretamente:

- regras de combate;
- economia;
- progressão;
- integridade do save;
- identidade dos itens;
- autoridade do servidor.

O sistema de regras permanece a fonte de verdade.

---

# 34. Ferramentas de desenvolvimento

## Principais

- Git
- GitHub
- Blender
- Substance 3D / alternativa equivalente
- Houdini para ferramentas e procedural quando necessário
- Photoshop / ferramentas de textura
- ferramentas de captura e edição de animação
- IDE/editor de código
- ferramenta de profiling

## IA

- Kashmir AI Studio
- modelos de linguagem
- geração de conceito
- geração de referências visuais
- ferramentas de análise de dados
- agentes de teste

---

# 35. Engine — decisão provisória

## Candidata A — Godot 4.6

Godot 4.6 é estável desde janeiro de 2026 e possui um novo framework de IK baseado em `SkeletonModifier3D`, com `TwoBoneIK3D`, `FABRIK3D`, `CCDIK3D`, `JacobianIK3D` e constraints. Também fornece AnimationTree, navegação 3D, ragdoll/PhysicalBone e suporte a multithreading. citeturn575083search3turn575083search9turn326286search0turn326286search1turn103462search2turn103462search12

Vantagens:

- open source;
- licença MIT;
- liberdade de modificação;
- excelente controle do código-fonte;
- baixo custo de entrada;
- sistema 3D suficientemente flexível;
- nova camada de IK muito relevante para o projeto;
- fácil integração com ferramentas próprias;
- excelente encaixe com a filosofia de Kashmir AI Studio. citeturn575083search0turn575083search1

Pontos de atenção:

- será necessário construir grande parte da infraestrutura que engines AAA já oferecem;
- animation/motion pipeline exigirá engenharia própria;
- tooling de produção de personagens e combate avançado precisará ser desenvolvido ou integrado;
- sistemas de grande escala exigirão arquitetura cuidadosa.

## Candidata B — Unreal Engine 5

Unreal oferece nativamente:

- Gameplay Ability System;
- Gameplay Attributes;
- Gameplay Effects;
- Ability Tasks;
- Control Rig;
- Full Body IK;
- Motion Warping;
- Motion Matching/Pose Search;
- Chaos Physics;
- MassEntity;
- sistemas de IA, navegação, StateTree e percepção. citeturn103462search0turn103462search1turn808150search0turn808150search6turn103462search14turn103462search8turn103462search3

Isso é altamente compatível com o problema técnico de KashmirAct.

Pontos de atenção:

- maior complexidade operacional;
- maior dependência do ecossistema Epic;
- maior peso de hardware/editor;
- licenciamento com royalty acima do limite atual informado pela Epic para jogos. citeturn313778search0turn313778search2

## Candidata C — Unity 6

Unity continua viável para um Action RPG e possui um ecossistema grande para runtime character systems, animation, physics e tooling. O Runtime Fee foi cancelado e não se aplica a jogos feitos com Unity 6. A precificação dos planos Pro/Enterprise mudou em 2026. citeturn313778search4

Porém, para o núcleo específico de:

**corpo + procedural animation + ability composition + high-end action combat**

Unreal e Godot devem ser investigadas primeiro.

---

# 36. Conclusão provisória da engine

**Godot não deve ser descartado.**

A recomendação desta fundação é:

> **Godot 4.6 como plataforma inicial de prototipagem do sistema. Unreal Engine 5 deve permanecer como candidata séria para produção caso o protótipo revele que animação procedural, motion matching, Control Rig e integração física são gargalos centrais.**

A decisão final deve acontecer por evidência, não por preferência.

---

# 37. Referências técnicas analisadas

## Projetos GitHub

### Relintai/Broken Seals
Projeto 3D third-person RPG baseado em Godot customizado, com single-player/multiplayer, classes, inventário, crafting, spell system, talentos, AI, terrain streaming/procedural generation, LOD e módulos próprios. É uma referência particularmente importante para arquitetura sistêmica em família Godot. citeturn997807search2

### SaranSundar/ActionRPGGodot
Referência de estrutura para Action RPG em Godot.

### DaebenDev/Sentinels-Spire
Mostra arquitetura modular baseada em FSM, componentes, hitbox/hurtbox e Ability System em Godot. citeturn997807search8

### Ryvos/Hollowfane
Demonstra RPG isométrico completo em Godot 4.6 com loot, crafting, classes, save schema, procedural dungeons e harness de bot-play para testes automatizados. A presença de `tools/bot_play.gd` é especialmente relevante para nossa futura infraestrutura de agentes de teste. citeturn997807search2

### kibble-cabal/ability-system
Framework de Ability System para Godot 4 inspirado no Gameplay Ability System da Unreal, com abilities, events, attributes, effects e tags. citeturn997807search2

### brunosrz/AbilitySystem
Implementação data-driven de abilities para Godot 4 com fases como Windup, Execution e Recovery. citeturn997807search3

### OctoD/godot-gameplay-systems
Arquitetura de abilities, containers, attributes e tags em Godot. citeturn997807search9

### andrewRCr/ActionRPGProject
Action RPG third-person em Unreal com equipamento modular, stamina, poise/stagger e AI combat director. citeturn997807search0

### ilchul1/UE5ActionRPG
Arquitetura moderna em Unreal com GAS, StateTree, Motion Matching e Motion Warping. citeturn997807search4

### FotisBaba/Action-RPG
Exemplo de Action RPG em UE5 utilizando C++/Blueprint e Gameplay Abilities. citeturn997807search5

### orangeduck/Motion-Matching
Referência técnica para motion matching e seleção de movimentos.

### Projeto de Unity de procedural animation
A pesquisa encontrou projetos de procedural animation e humanoid procedural animation úteis como referência algorítmica, independentemente da engine.

---

# 38. Referências de design

## Overgeared

A análise do sistema de criação de *Overgeared* confirma que uma parte central da fantasia está em:

- criação de métodos de produção;
- influência da forma;
- materiais;
- habilidade do artesão;
- descrição das características;
- autoria;
- qualidade;
- reputação;
- descoberta de itens;
- evolução das habilidades de produção. citeturn315277search0turn315277search1turn315277search5turn315277search7

KashmirAct deve transformar esses conceitos em sistemas próprios e simuláveis.

---

# 39. Referências de sistemas sandbox

ArcheAge demonstra a utilidade de separar habilidades/profissões e permitir combinações para criar múltiplos arquétipos de personagem. citeturn608814search3

A ideia de produção profunda também aparece em sistemas de forging que usam qualidade, blueprint, materiais e execução como variáveis do resultado. citeturn608814search0turn608814search4

Esses padrões serão usados apenas como referência de design.

---

# 40. Arquitetura macro proposta

```text
KASHMIRACT
│
├── CORE
│   ├── Rules
│   ├── Deterministic Simulation
│   ├── Data
│   └── Save System
│
├── CHARACTER
│   ├── Movement
│   ├── Body Controller
│   ├── Animation
│   ├── IK
│   ├── Attributes
│   └── Behavior Profile
│
├── COMBAT
│   ├── Input
│   ├── Motion Primitives
│   ├── Ability Composer
│   ├── Hit Detection
│   ├── Damage
│   ├── Effects
│   └── Combat Telemetry
│
├── CREATION
│   ├── Item Designer
│   ├── Material System
│   ├── Crafting
│   ├── Blueprint
│   ├── Quality
│   ├── Item Evolution
│   └── Ownership
│
├── PROFESSION
│   ├── Knowledge
│   ├── Mastery
│   ├── Specialization
│   └── Discovery
│
├── WORLD
│   ├── NPC
│   ├── Factions
│   ├── Reputation
│   ├── Economy
│   └── Events
│
├── AI
│   ├── Runtime AI
│   ├── Analysis Agent
│   ├── Discovery Agent
│   ├── Simulation Agent
│   └── Testing Bots
│
└── TOOLS
    ├── Debug
    ├── Telemetry
    ├── Editors
    ├── Data Viewer
    └── AI Studio Integration
```

---

# 41. Primeiro protótipo obrigatório

Não começar por mundo.

Não começar por lore.

Não começar por dezenas de classes.

Não começar por produção de assets em massa.

## Prototype P0

Uma pequena arena.

### Conteúdo

- 1 personagem humanoide;
- 1 espada;
- 1 inimigo;
- câmera third-person;
- locomotion;
- dodge;
- block;
- parry;
- 3 motion primitives;
- 3 attacks;
- hit detection;
- stamina;
- damage;
- procedural hand IK;
- weapon alignment;
- combat telemetry.

Depois:

### P1

Adicionar:

- Ability Composer;
- Skill Graph;
- Candidate Generator;
- Combat Simulator;
- Discovery Agent.

Depois:

### P2

Adicionar:

- profissão Blacksmith;
- materiais;
- criação de uma espada;
- qualidade;
- blueprint;
- item identity;
- histórico do item.

Depois:

### P3

Adicionar:

- segundo jogador/personagem de teste;
- estilos diferentes;
- descoberta de arquétipos;
- NPC;
- reputação.

---

# 42. Critério de sucesso do primeiro protótipo

O protótipo será considerado tecnicamente promissor quando:

1. o jogador puder atacar de formas diferentes com a mesma arma;
2. pequenas diferenças de movimento produzirem resultados perceptíveis;
3. o sistema registrar o comportamento do jogador;
4. o agente puder gerar candidatos coerentes;
5. os candidatos puderem ser simulados;
6. pelo menos uma nova técnica puder ser descoberta pelo comportamento do jogador;
7. a técnica puder ser salva como dado;
8. a técnica puder ser reutilizada no gameplay;
9. uma arma criada pelo jogador possuir propriedades originadas das decisões de criação;
10. dois personagens produzidos por estilos diferentes apresentarem diferenças mecânicas observáveis.

---

# 43. Princípio de desenvolvimento

Todo desenvolvimento deve obedecer:

**Sistema antes de conteúdo.**

**Dados antes de interface.**

**Simulação antes de efeitos.**

**Protótipo antes de produção.**

**Métrica antes de opinião.**

**Regra determinística antes de IA generativa.**

**Evidência antes de declarar sucesso.**

---

# 44. Decisão da Fundação v0.1

### Confirmado

- nome de desenvolvimento: **KashmirAct**;
- projeto independente do Kashmir anterior;
- experiência inspirada em Overgeared sem VR;
- Action RPG 3D;
- terceira pessoa;
- combate em tempo real;
- progressão baseada no comportamento;
- classes emergentes;
- profissões;
- criação profunda de equipamentos;
- criação/composição de habilidades;
- IA de descoberta;
- telemetria de combate;
- simulação de candidatos;
- autoria e histórico de itens.

### Provisório

- Godot 4.6;
- single-player como primeiro alvo;
- multiplayer futuro;
- mundo aberto;
- arquitetura final de rede;
- formato final de câmera e lock-on;
- lista definitiva de profissões.

### Fora do escopo inicial

- VR;
- MMO completo;
- dezenas de mapas;
- centenas de NPCs;
- crafting de todas as categorias;
- narrativa extensa;
- produção final de arte.

---

# 45. Princípio final

KashmirAct não deve tentar ser um RPG com muitas opções.

Deve ser:

> **um sistema no qual as opções emergem da interação entre jogador, personagem, equipamento, profissão, mundo e experimentação.**

A ambição técnica principal é permitir:

**PLAYER ACTION**
→ **BEHAVIOR**
→ **MASTERY**
→ **EXPERIMENTATION**
→ **DISCOVERY**
→ **CREATION**
→ **IDENTITY**

Esse ciclo é o núcleo do jogo.
