# TLIM - Tibia Loot & Inventory Manager

Aplicação web para auxiliar jogadores de Tibia na gestão de recursos pós-hunt e no acompanhamento de progressão de Bestiário.

## Sobre o projeto

Este projeto faz parte de um portifólio de migração de carreira (Analista -> Desenvolvedor) e está sendo construído em 3 etapas progressivas:

| Etapa | Stack | Status |
|-------|-------|--------|
| Etapa 1 - MVP | Python + FastAPI + SQLite | 🚧 Em desenvolvimento |
| Etapa 2 - Reescrita | Java + Spring Boot + PostgreSQL | ⏳ Pendente |
| Etapa 3 - Frontend | React.js | ⏳ Pendente|

## Funcionalidades

- 📦 **Gestão de inventário** - Controle de itens para Imbuements, Quest, Addons e Weekly Task
- 💰 **Motor de Decisão de Venda** - Compara preços NPC vs Market automaticamente
- 🐾 **Tracker de Bestiário** - Monitora kills e progresso de cada criatura
- ✨ **Calculadora de Charms** - Sugere quais criaturas caças para atingir o charm desejado
- 📥 **Importação de Hunt** - aceita JSON do Hunt Analyser ou texto colado do jogo

## Tecnologias - Etapa 1

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2

## Como Rodar Localmente

**Pré-requisitos:** Python 3.11+

```bash
# Clonar o repositório
git clone https://github.com/calgadev/tlim-python.git
cd tlim-python

# Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install fastapi uvicorn sqlalchemy jinja2 python-multipar aiofiles

# Populas o banco com dados iniciais
python3 seed.py

# Iniciar o servidor
uvicorn main:app --reloar

```

Acesse https://localhost:8000 para ver a aplicação.
Acesse http://localhost:8000/docs para a documentação interativa da API

## Status do Desenvolvimento

### Etapa 1 - Python + FastAPI
- [x] Setup do projeto e ambiente virtual
- [x] Configuração do banco de dados SQLite
- [x] Modelos: Item, Creature, UserInventory, BestiaryEntry
- [x] Seed data de itens e criaturas
- [x] Endpoints de listagem de itens e criaturas
- [x] Parser JSON do Hunt Analyser
- [x] Parser de texto (Regex)
- [x] Motor de Decisão de Venda
- [ ] Tracker de Bestiário
- [ ] Calculadora de Charms
- [ ] Interface HTML com Jinja2

## Backlog -  Funcionalidades futuras

### Etapa 2 Java + Spring Boot
- [ ] **Weekly Task Tracker** - O jogo possui aproximadamente 460 itens que podem ser entregues em Delivery Task semanal. O sistema deverá identificar a adicionar essa decisão ao motor de decisão de vendas, para sinalizar ao jogador itens que ele pode guardar para tasks futuras