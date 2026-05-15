# 📊 Dashboard de Obras Públicas DER-MG
## Portfólio de Engenharia de Dados

---

## 👤 Sobre o Projeto

**Desenvolvido por:** Cristiane  
**Data:** Maio 2026  
**Objetivo:** Demonstrar habilidades em Engenharia de Dados, ETL e Visualização de Dados

---

## 🎯 Visão Geral

Este projeto é um **dashboard interativo completo** para análise de obras públicas do Departamento de Estradas de Rodagem de Minas Gerais (DER-MG), desenvolvido como portfólio profissional.

### Tecnologias Utilizadas

- **Python 3.11+** - Linguagem principal
- **Pandas & NumPy** - Manipulação e análise de dados
- **Streamlit** - Framework para dashboard interativo
- **Plotly** - Visualizações interativas
- **Folium** - Mapas geolocalizados
- **BeautifulSoup4** - Web scraping
- **Git & GitHub** - Controle de versão

---

## 🏗️ Arquitetura do Projeto

### Pipeline ETL Completo

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   EXTRACT   │────▶│  TRANSFORM   │────▶│    LOAD     │
│             │     │              │     │             │
│ • Web Scraping   │ • Normalização    │ • CSV/Parquet │
│ • APIs           │ • Limpeza         │ • Metadados   │
│ • Dados Simulados│ • Enriquecimento  │ • Relatórios  │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
                                    ┌──────────────────────┐
                                    │  DASHBOARD STREAMLIT │
                                    │                      │
                                    │ • Visão Geral        │
                                    │ • Análises           │
                                    │ • Mapa Interativo    │
                                    └──────────────────────┘
```

---

## 📈 Funcionalidades Implementadas

### 1. ETL (Extract, Transform, Load)

#### Extract
- ✅ Web scraping de dados públicos
- ✅ Geração de dados simulados realistas
- ✅ Validação e tratamento de erros
- ✅ Logging detalhado do processo

#### Transform
- ✅ Normalização de colunas (snake_case)
- ✅ Conversão de tipos de dados
- ✅ Cálculo de métricas derivadas:
  - Status semáforo (verde/amarelo/vermelho)
  - Percentual de execução vs prazo
  - Valor executado
  - Categoria de valor
- ✅ Tratamento de valores nulos
- ✅ Flags de qualidade dos dados

#### Load
- ✅ Salvamento em múltiplos formatos (CSV, Parquet)
- ✅ Geração de metadados JSON
- ✅ Relatórios de qualidade automatizados
- ✅ Tabelas agregadas para análises rápidas

### 2. Dashboard Interativo

#### Página 1: Visão Geral
- 📊 KPIs principais (total obras, valor, execução, atrasos)
- 📈 Gráfico de pizza: distribuição por status
- 🚦 Gráfico de barras: status semáforo
- 🗺️ Gráfico de barras: obras por região

#### Página 2: Análises Detalhadas
- 💰 Scatter plot: valor vs execução
- 📅 Evolução temporal de obras
- 🏗️ Análise por tipo de obra
- 📋 Tabela interativa com filtros
- 📥 Download de dados em CSV

#### Página 3: Mapa Geolocalizado
- 🗺️ Mapa interativo com Folium
- 📍 Marcadores coloridos por status
- 💬 Popups com detalhes de cada obra
- 📊 Estatísticas do mapa

### 3. Filtros Dinâmicos

- 🔍 Região (todas as regiões do DER-MG)
- ✅ Status da obra (múltipla seleção)
- 💵 Faixa de valor do contrato (slider)
- 📅 Intervalo de datas de início

---

## 📊 Resultados do Processamento

### Estatísticas dos Dados

- **Total de Obras:** 150
- **Valor Total:** R$ 1.073.836.597,94
- **Regiões Cobertas:** 9
- **Tipos de Obra:** 7
- **Completude dos Dados:** 100%
- **Geolocalização:** 100%

### Distribuição por Status Semáforo

- 🔴 **Vermelho (Atrasadas):** 64 obras (42.7%)
- 🟢 **Verde (No prazo):** 43 obras (28.7%)
- 🔵 **Azul (Em licitação):** 41 obras (27.3%)
- 🟡 **Amarelo (Atraso moderado):** 2 obras (1.3%)

---

## 💡 Diferenciais Técnicos

### Boas Práticas de Código

✅ **Código Modular:** Separação clara de responsabilidades (ETL, Dashboard)  
✅ **Documentação:** Docstrings em todas as funções  
✅ **Type Hints:** Tipagem para melhor manutenibilidade  
✅ **Error Handling:** Tratamento robusto de exceções  
✅ **Logging:** Rastreamento detalhado de processos  

### Qualidade de Dados

✅ **Validação:** Verificação de integridade dos dados  
✅ **Normalização:** Padronização de formatos  
✅ **Enriquecimento:** Cálculo de métricas derivadas  
✅ **Metadados:** Documentação automática do dataset  

### Performance

✅ **Caching:** Uso de @st.cache_data no Streamlit  
✅ **Parquet:** Formato otimizado para grandes volumes  
✅ **Lazy Loading:** Carregamento sob demanda  

---

## 🚀 Como Executar

### Instalação

```bash
# Clone o repositório
git clone https://github.com/cristiane/der-mg-obras-dashboard.git
cd der-mg-obras-dashboard

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
```

### Execução

```bash
# Execute o pipeline ETL
python run_etl.py

# Inicie o dashboard
streamlit run dashboard/app.py
```

### Acesso

O dashboard estará disponível em: **http://localhost:8501**

---

## 📁 Estrutura do Projeto

```
der-mg-obras-dashboard/
├── README.md                 # Documentação principal
├── APRESENTACAO_PORTFOLIO.md # Este documento
├── requirements.txt          # Dependências
├── .gitignore               # Arquivos ignorados
├── run_etl.py               # Pipeline completo
│
├── etl/                     # Módulos ETL
│   ├── __init__.py
│   ├── extract.py           # Extração
│   ├── transform.py         # Transformação
│   └── load.py              # Carga
│
├── data/processed/          # Dados processados
│   ├── obras_processadas.csv
│   ├── obras_processadas.parquet
│   ├── metadata.json
│   └── quality_report.txt
│
├── dashboard/               # Dashboard
│   └── app.py              # Aplicação Streamlit
│
└── deploy/                  # Deploy
    └── Procfile            # Streamlit Cloud
```

---

## 🎓 Competências Demonstradas

### Engenharia de Dados

- ✅ Design e implementação de pipelines ETL
- ✅ Modelagem e transformação de dados
- ✅ Otimização de performance
- ✅ Qualidade e governança de dados

### Análise de Dados

- ✅ Análise exploratória de dados (EDA)
- ✅ Cálculo de métricas e KPIs
- ✅ Identificação de padrões e insights
- ✅ Visualização de dados

### Desenvolvimento

- ✅ Python avançado (OOP, type hints)
- ✅ Controle de versão com Git
- ✅ Documentação técnica
- ✅ Deploy de aplicações

### Soft Skills

- ✅ Resolução de problemas
- ✅ Atenção aos detalhes
- ✅ Comunicação técnica
- ✅ Autonomia e proatividade

---

## 🌐 Links

- **Repositório GitHub:** https://github.com/cristiane/der-mg-obras-dashboard
- **Dashboard Online:** [Em breve no Streamlit Cloud]
- **LinkedIn:** [Seu LinkedIn]
- **Portfolio:** [Seu Portfolio]

---

## 📞 Contato

**Cristiane**  
📧 Email: cristiane@example.com  
💼 LinkedIn: linkedin.com/in/cristiane  
🐙 GitHub: github.com/cristiane

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Desenvolvido com ❤️ e Python | 2026**