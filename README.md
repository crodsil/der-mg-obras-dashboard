# 🚧 Dashboard de Obras Públicas DER-MG

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

Dashboard interativo para análise e visualização de obras públicas do Departamento de Estradas de Rodagem de Minas Gerais (DER-MG).

![Dashboard Preview](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Dashboard+DER-MG+Preview)

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como portfólio profissional de Engenharia de Dados, demonstrando habilidades em:

- **ETL (Extract, Transform, Load)**: Pipeline completo de processamento de dados
- **Análise de Dados**: Transformações, limpeza e enriquecimento
- **Visualização**: Dashboard interativo com Streamlit
- **Boas Práticas**: Código limpo, documentado e modular

### 🎯 Funcionalidades

- ✅ Extração de dados de obras públicas (web scraping + dados simulados)
- ✅ Transformação e limpeza de dados com pandas
- ✅ Cálculo de métricas derivadas (status semáforo, execução vs prazo)
- ✅ Dashboard interativo com múltiplas visualizações
- ✅ Filtros dinâmicos (região, status, valor, data)
- ✅ Mapa geolocalizado de obras
- ✅ Exportação de dados em CSV

## 🚀 Como Rodar Localmente

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/der-mg-obras-dashboard.git
cd der-mg-obras-dashboard
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### Executando o Pipeline ETL

Execute o pipeline completo para processar os dados:

```bash
# Opção 1: Script único
python run_etl.py

# Opção 2: Executar etapas individualmente
python etl/extract.py    # Extração
python etl/transform.py  # Transformação
python etl/load.py       # Carga
```

### Executando o Dashboard

```bash
streamlit run dashboard/app.py
```

O dashboard estará disponível em: `http://localhost:8501`

## 📊 Estrutura do Projeto

```
der-mg-obras-dashboard/
├── README.md                 # Documentação principal
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados pelo Git
├── run_etl.py               # Script para executar pipeline completo
│
├── etl/                     # Módulos ETL
│   ├── __init__.py
│   ├── extract.py           # Extração de dados
│   ├── transform.py         # Transformação e limpeza
│   └── load.py              # Carga e persistência
│
├── data/                    # Dados processados
│   └── processed/
│       ├── obras_processadas.csv
│       ├── obras_processadas.parquet
│       ├── metadata.json
│       └── quality_report.txt
│
├── dashboard/               # Dashboard Streamlit
│   └── app.py              # Aplicação principal
│
└── deploy/                  # Configurações de deploy
    └── Procfile            # Para Streamlit Cloud
```

## 🔄 Metodologia do ETL

### 1. Extract (Extração)

- **Fonte primária**: Portal da Transparência MG
- **Fonte secundária**: Site oficial DER-MG
- **Fallback**: Dados simulados realistas para demonstração
- **Formato**: CSV bruto

### 2. Transform (Transformação)

Aplicamos as seguintes transformações:

- ✅ Normalização de colunas (snake_case, sem acentos)
- ✅ Conversão de valores monetários (R$ → float)
- ✅ Conversão de datas (string → datetime)
- ✅ Cálculo de campos derivados:
  - `percentual_execucao`: % de execução da obra
  - `status_semaforo`: verde/amarelo/vermelho baseado em prazo
  - `data_prevista_conclusao`: data estimada de término
  - `dias_desde_inicio`: tempo decorrido
  - `valor_executado`: valor já gasto
  - `categoria_valor`: classificação por faixa de valor
- ✅ Tratamento de valores nulos com estratégias documentadas
- ✅ Flags de qualidade dos dados

### 3. Load (Carga)

Dados salvos em múltiplos formatos:

- **CSV**: Para compatibilidade universal
- **Parquet**: Para performance otimizada
- **JSON**: Metadados e estatísticas
- **TXT**: Relatório de qualidade

## 📈 Dashboard - Páginas

### 1. 📊 Visão Geral

- KPIs principais (total obras, valor, execução média, obras atrasadas)
- Distribuição por status
- Status semáforo (verde/amarelo/vermelho)
- Obras por região

### 2. 📈 Análises

- Scatter plot: Valor vs Execução
- Evolução temporal de obras
- Análise por tipo de obra
- Tabela interativa com filtros
- Download de dados em CSV

### 3. 🗺️ Mapa

- Mapa interativo com obras geolocalizadas
- Marcadores coloridos por status semáforo
- Popup com detalhes de cada obra
- Estatísticas do mapa

## 🎨 Filtros Disponíveis

- **Região**: Todas as regiões do DER-MG
- **Status**: Em andamento, Concluída, Paralisada, Em licitação
- **Valor do Contrato**: Slider com faixa de valores
- **Período de Início**: Intervalo de datas

## 📦 Fonte dos Dados

### Fontes Oficiais

| Fonte | Link | Formato |
|-------|------|---------|
| Portal da Transparência MG | [transparencia.mg.gov.br](https://www.transparencia.mg.gov.br) | Web/CSV |
| DER-MG Obras Públicas | [der.mg.gov.br/transparencia/obras-publicas](https://www.der.mg.gov.br/transparencia/obras-publicas) | Web |
| Dados Abertos DER-MG | [der.mg.gov.br/transparencia/dados-abertos](https://www.der.mg.gov.br/transparencia/dados-abertos) | CSV |

### Dados Simulados

Para fins de demonstração, o projeto inclui geração de dados simulados realistas quando as fontes oficiais não estão disponíveis. Os dados simulados seguem a mesma estrutura dos dados reais.

## 🚀 Deploy no Streamlit Cloud

### Passo a Passo

1. **Faça fork deste repositório**

2. **Acesse [share.streamlit.io](https://share.streamlit.io)**

3. **Clique em "New app"**

4. **Configure:**
   - Repository: `seu-usuario/der-mg-obras-dashboard`
   - Branch: `main`
   - Main file path: `dashboard/app.py`

5. **Clique em "Deploy"**

Seu dashboard estará online em poucos minutos! 🎉

### Variáveis de Ambiente (Opcional)

Se você adicionar autenticação ou APIs externas, configure no Streamlit Cloud:

```
Settings → Secrets → Edit Secrets
```

## 🛠️ Stack Técnica

- **Python 3.11+**: Linguagem principal
- **pandas**: Manipulação de dados
- **numpy**: Operações numéricas
- **requests**: Requisições HTTP
- **BeautifulSoup4**: Web scraping
- **streamlit**: Framework do dashboard
- **plotly**: Gráficos interativos
- **folium**: Mapas interativos
- **pyarrow**: Formato Parquet

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Cristiane**

- GitHub: [@cristiane](https://github.com/cristiane)
- LinkedIn: [Cristiane](https://linkedin.com/in/cristiane)
- Email: cristiane@example.com

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📞 Suporte

Se você tiver alguma dúvida ou sugestão, abra uma [issue](https://github.com/seu-usuario/der-mg-obras-dashboard/issues).

## ⭐ Mostre seu apoio

Se este projeto foi útil para você, considere dar uma ⭐!

---

**Desenvolvido com ❤️ por Cristiane | 2026**