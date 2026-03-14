# TLIM — Tibia Loot & Inventory Manager

Aplicação web para auxiliar jogadores de Tibia na gestão de recursos pós-hunt
e no acompanhamento de progressão de Bestiário.

> **Projeto de portfólio** desenvolvido durante migração de carreira de Analista de Sistemas
> para Desenvolvedor. Construído em etapas progressivas para demonstrar evolução técnica.

---

## 🗺️ Roadmap do Projeto

| Etapa | Stack | Status |
|-------|-------|--------|
| Etapa 1 — MVP | Python + FastAPI + SQLite + Jinja2 | ✅ Concluída |
| Etapa 2 — Reescrita | Java 17 + Spring Boot + PostgreSQL | 🔜 Próxima |
| Etapa 3 — Frontend | React.js | ⏳ Pendente |

---

## 📋 Sobre o Projeto

O TLIM resolve três problemas reais de jogadores de Tibia:

- **Decisão de venda**: após uma hunt, o jogador não sabe se deve vender ou guardar cada item.
O sistema compara preços de NPC vs Market e verifica metas de estoque pessoal automaticamente.
- **Rastreio de Bestiário**: controlar manualmente quantas kills foram feitas por criatura é
trabalhoso. O TLIM atualiza o progresso automaticamente a cada hunt importada.
- **Planejamento de Charms**: a Calculadora de Charms sugere quais criaturas caçar para
atingir o charm desejado, priorizando as mais próximas de completar.

---

## ✅ Etapa 1 — Python + FastAPI

### Funcionalidades implementadas

- 📥 **Importação de Hunt** — aceita arquivo `.json` do Hunt Analyser ou texto colado do jogo
- 💰 **Motor de Decisão de Venda** — 5 regras de prioridade: meta de estoque → imbuement → NPC → market → verificar
- 🐾 **Tracker de Bestiário** — atualiza kills automaticamente a cada importação
- ✨ **Calculadora de Charms** — sugere criaturas ordenadas por kills restantes
- 📦 **Gestão de Inventário** — estoque com metas de quantidade por item
- 📖 **Documentação automática** — Swagger UI disponível em `/docs`

### Stack

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.12 |
| Framework | FastAPI 0.135 |
| Banco de dados | SQLite |
| ORM | SQLAlchemy 2.0 |
| Templates | Jinja2 |
| Servidor | Uvicorn |
| Validação | Pydantic v2 |

### Como rodar localmente

**Pré-requisitos:** Python 3.11+, Git
```bash
# 1. Clonar o repositório
git clone https://github.com/calgadev/tlim-python.git
cd tlim-python

# 2. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependências
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart aiofiles

# 4. Popular o banco com dados iniciais
python3 seed.py

# 5. Iniciar o servidor
uvicorn main:app --reload
```

- Interface web: **http://localhost:8000**
- Documentação da API: **http://localhost:8000/docs**

### Estrutura do projeto
```
tlim-python/
├── main.py                  ← Ponto de entrada e rotas HTML
├── seed.py                  ← Script de dados iniciais
├── routers/                 ← Endpoints REST da API
├── services/                ← Regras de negócio
│   ├── sale_decision_service.py   ← Motor de decisão de venda
│   ├── bestiary_service.py        ← Tracker de bestiário
│   └── charm_calculator_service.py← Calculadora de charms
├── parsers/                 ← Interpretação de dados brutos
│   ├── json_hunt_parser.py        ← Arquivo .json do Hunt Analyser
│   └── text_hunt_parser.py        ← Log em texto puro (Regex)
├── models/                  ← Modelos do banco de dados
├── schemas/                 ← Validação de dados (Pydantic)
├── templates/               ← Interface HTML (Jinja2)
└── seed_data/               ← Dados iniciais de itens e criaturas
```

---

## 🔮 Backlog — Funcionalidades Futuras

### Etapa 2 — Java + Spring Boot
- [ ] **Reescrita completa do backend** em Java 17 + Spring Boot + PostgreSQL
- [ ] **Scraping automático** da TibiaWiki para popular o catálogo de itens e criaturas
- [ ] **Weekly Task Tracker** — ~460 itens podem ser entregues em Weekly Tasks.
O Motor de Decisão deve recomendar guardar itens necessários para tasks ativas
- [ ] **Sistema de Charms atualizado** — Major Charms (desbloqueados com Charm Points
de Bestiário) e Minor Charms (desbloqueados pelos Major Charms), cada um com
três níveis de custo progressivo

### Etapa 3 — React
- [ ] **Frontend moderno** substituindo os templates Jinja2
- [ ] **Deploy online** — backend no Railway, frontend no Vercel

---

## 💡 Decisões Técnicas

**Por que Python na Etapa 1?**
O projeto é desenvolvido por um analista de sistemas migrando para desenvolvimento.
Python foi escolhido para a primeira etapa por permitir entregas rápidas e validar a
lógica de negócio antes de aprender um framework mais complexo.

**Por que Java na Etapa 2?**
Java + Spring Boot é a stack dominante em empresas brasileiras de médio e grande porte.
Reescrever o mesmo projeto em Java demonstra que o conhecimento é transferível entre
linguagens — não apenas decorado.

**Por que a abordagem em etapas?**
Três repositórios com a mesma lógica em stacks diferentes demonstram evolução técnica
real e capacidade de tomar decisões arquiteturais conscientes.
