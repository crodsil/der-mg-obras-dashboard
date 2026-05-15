"""
Dashboard Interativo de Obras Públicas do DER-MG
Autor: Cristiane
Data: 2026-05-15
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import folium
from streamlit_folium import folium_static
import json

# Configuração da página
st.set_page_config(
    page_title="DER-MG - Dashboard de Obras",
    page_icon="🚧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .stMetric label {
        color: #ffffff !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #4CAF50 !important;
        font-size: 2rem !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #ff9800 !important;
    }
    h1 {
        color: #4CAF50;
    }
    h2, h3 {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega dados processados ou gera dados simulados"""
    data_path = Path(__file__).parent.parent / "data" / "processed" / "obras_processadas.csv"
    
    if not data_path.exists():
        df = generate_sample_data()
    else:
        df = pd.read_csv(data_path)
    
    # Converte datas
    date_cols = ['data_inicio', 'data_prevista_conclusao', 'data_extracao']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

def generate_sample_data():
    """Gera dados simulados para demonstração"""
    import random
    from datetime import datetime, timedelta
    
    regioes = ['Belo Horizonte', 'Juiz de Fora', 'Montes Claros', 'Uberlândia',
               'Governador Valadares', 'Varginha', 'Uberaba', 'Patos de Minas', 'Teófilo Otoni']
    status_opcoes = ['Em andamento', 'Concluída', 'Paralisada', 'Em licitação']
    tipos_obra = ['Pavimentação', 'Restauração', 'Duplicação', 'Ponte', 'Viaduto', 'Sinalização', 'Drenagem']
    
    data = []
    for i in range(1, 151):
        regiao = random.choice(regioes)
        tipo = random.choice(tipos_obra)
        status = random.choice(status_opcoes)
        valor_contrato = random.uniform(500000, 15000000)
        percentual_execucao = random.uniform(0, 100) if status != 'Em licitação' else 0
        ano_inicio = random.randint(2020, 2024)
        mes_inicio = random.randint(1, 12)
        data_inicio = f"{ano_inicio}-{mes_inicio:02d}-{random.randint(1, 28):02d}"
        prazo_meses = random.randint(6, 36)
        rodovia = f"MG-{random.randint(10, 999):03d}"
        latitude = random.uniform(-22.5, -15.0)
        longitude = random.uniform(-51.0, -40.0)
        
        # Calcula status semáforo
        if status == 'Paralisada':
            status_semaforo = 'vermelho'
        elif status == 'Concluída':
            status_semaforo = 'verde'
        elif status == 'Em licitação':
            status_semaforo = 'azul'
        else:
            if percentual_execucao >= 70:
                status_semaforo = 'verde'
            elif percentual_execucao >= 40:
                status_semaforo = 'amarelo'
            else:
                status_semaforo = 'vermelho'
        
        obra = {
            'id_obra': f'DER-{i:04d}',
            'nome_obra': f'{tipo} {rodovia} - Trecho {regiao}',
            'tipo_obra': tipo,
            'regiao': regiao,
            'rodovia': rodovia,
            'status': status,
            'valor_contrato': valor_contrato,
            'percentual_execucao': percentual_execucao,
            'data_inicio': data_inicio,
            'prazo_meses': prazo_meses,
            'empresa_contratada': f'Construtora {random.choice(["Alpha", "Beta", "Gamma", "Delta", "Omega"])} Ltda',
            'latitude': latitude,
            'longitude': longitude,
            'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status_semaforo': status_semaforo,
            'dados_completos': True,
            'tem_geolocalizacao': True,
            'obra_recente': ano_inicio >= 2022,
            'dias_desde_inicio': random.randint(0, 1000),
            'data_prevista_conclusao': (datetime.strptime(data_inicio, '%Y-%m-%d') + timedelta(days=prazo_meses*30)).strftime('%Y-%m-%d'),
            'valor_executado': valor_contrato * (percentual_execucao / 100),
            'categoria_valor': 'Grande' if valor_contrato > 5000000 else 'Médio' if valor_contrato > 1000000 else 'Pequeno'
        }
        data.append(obra)
    
    return pd.DataFrame(data)

@st.cache_data
def load_metadata():
    """Carrega metadados"""
    metadata_path = Path(__file__).parent.parent / "data" / "processed" / "metadata.json"
    
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def apply_filters(df):
    """Aplica filtros da sidebar"""
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de região
    regioes = ['Todas'] + sorted(df['regiao'].unique().tolist())
    regiao_selecionada = st.sidebar.selectbox("Região", regioes)
    
    if regiao_selecionada != 'Todas':
        df = df[df['regiao'] == regiao_selecionada]
    
    # Filtro de status
    status_opcoes = ['Todos'] + sorted(df['status'].unique().tolist())
    status_selecionado = st.sidebar.multiselect(
        "Status da Obra",
        status_opcoes[1:],
        default=status_opcoes[1:]
    )
    
    if status_selecionado:
        df = df[df['status'].isin(status_selecionado)]
    
    # Filtro de valor
    st.sidebar.subheader("Valor do Contrato")
    valor_min = float(df['valor_contrato'].min())
    valor_max = float(df['valor_contrato'].max())
    
    valor_range = st.sidebar.slider(
        "Faixa de valor (R$)",
        valor_min,
        valor_max,
        (valor_min, valor_max),
        format="R$ %.0f"
    )
    
    df = df[(df['valor_contrato'] >= valor_range[0]) & (df['valor_contrato'] <= valor_range[1])]
    
    # Filtro de data
    if 'data_inicio' in df.columns and df['data_inicio'].notna().any():
        st.sidebar.subheader("Período de Início")
        data_min = df['data_inicio'].min()
        data_max = df['data_inicio'].max()
        
        data_range = st.sidebar.date_input(
            "Intervalo de datas",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max
        )
        
        if len(data_range) == 2:
            df = df[(df['data_inicio'] >= pd.Timestamp(data_range[0])) & 
                   (df['data_inicio'] <= pd.Timestamp(data_range[1]))]
    
    return df

def show_kpis(df):
    """Exibe KPIs principais"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Obras",
            f"{len(df):,}",
            help="Número total de obras no período selecionado"
        )
    
    with col2:
        valor_total = df['valor_contrato'].sum()
        st.metric(
            "Valor Total Contratado",
            f"R$ {valor_total/1e6:.1f}M",
            help="Soma de todos os contratos"
        )
    
    with col3:
        exec_media = df['percentual_execucao'].mean()
        st.metric(
            "Execução Média",
            f"{exec_media:.1f}%",
            help="Percentual médio de execução das obras"
        )
    
    with col4:
        obras_atrasadas = len(df[df['status_semaforo'] == 'vermelho'])
        st.metric(
            "Obras Atrasadas",
            f"{obras_atrasadas}",
            delta=f"-{obras_atrasadas/len(df)*100:.1f}%",
            delta_color="inverse",
            help="Obras com status semáforo vermelho"
        )

def page_visao_geral(df):
    """Página 1: Visão Geral"""
    st.title("🏗️ Dashboard de Obras Públicas DER-MG")
    st.markdown("---")
    
    # KPIs
    show_kpis(df)
    
    st.markdown("---")
    
    # Gráficos em duas colunas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribuição por Status")
        status_counts = df['status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Obras por Status",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🚦 Status Semáforo")
        semaforo_counts = df['status_semaforo'].value_counts()
        cores = {
            'verde': '#28a745',
            'amarelo': '#ffc107',
            'vermelho': '#dc3545',
            'azul': '#007bff'
        }
        fig = go.Figure(data=[go.Bar(
            x=semaforo_counts.index,
            y=semaforo_counts.values,
            marker_color=[cores.get(x, '#6c757d') for x in semaforo_counts.index],
            text=semaforo_counts.values,
            textposition='auto'
        )])
        fig.update_layout(
            title="Distribuição por Status Semáforo",
            xaxis_title="Status",
            yaxis_title="Quantidade de Obras"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de barras - Obras por região
    st.subheader("🗺️ Obras por Região")
    regiao_counts = df['regiao'].value_counts().head(10)
    fig = px.bar(
        x=regiao_counts.values,
        y=regiao_counts.index,
        orientation='h',
        title="Top 10 Regiões com Mais Obras",
        labels={'x': 'Quantidade', 'y': 'Região'},
        color=regiao_counts.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

def page_analises(df):
    """Página 2: Análises Detalhadas"""
    st.title("📈 Análises Detalhadas")
    st.markdown("---")
    
    # Scatter plot: Valor vs Execução
    st.subheader("💰 Valor do Contrato vs Execução")
    fig = px.scatter(
        df,
        x='valor_contrato',
        y='percentual_execucao',
        color='status',
        size='valor_contrato',
        hover_data=['nome_obra', 'regiao'],
        title="Relação entre Valor Contratado e Percentual de Execução",
        labels={
            'valor_contrato': 'Valor do Contrato (R$)',
            'percentual_execucao': 'Execução (%)'
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise temporal
    if 'data_inicio' in df.columns and df['data_inicio'].notna().any():
        st.subheader("📅 Evolução Temporal")
        df_temporal = df.copy()
        df_temporal['ano_mes'] = df_temporal['data_inicio'].dt.to_period('M').astype(str)
        obras_por_mes = df_temporal.groupby('ano_mes').size().reset_index(name='quantidade')
        
        fig = px.line(
            obras_por_mes,
            x='ano_mes',
            y='quantidade',
            title="Obras Iniciadas por Mês",
            markers=True
        )
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise por tipo de obra
    st.subheader("🏗️ Análise por Tipo de Obra")
    col1, col2 = st.columns(2)
    
    with col1:
        tipo_counts = df['tipo_obra'].value_counts()
        fig = px.bar(
            x=tipo_counts.index,
            y=tipo_counts.values,
            title="Quantidade por Tipo de Obra",
            labels={'x': 'Tipo', 'y': 'Quantidade'},
            color=tipo_counts.values,
            color_continuous_scale='Viridis'
        )
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        tipo_valor = df.groupby('tipo_obra')['valor_contrato'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=tipo_valor.index,
            y=tipo_valor.values / 1e6,
            title="Valor Total por Tipo de Obra (R$ Milhões)",
            labels={'x': 'Tipo', 'y': 'Valor (R$ Milhões)'},
            color=tipo_valor.values,
            color_continuous_scale='Reds'
        )
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela interativa
    st.subheader("📋 Tabela de Obras")
    
    # Seleção de colunas para exibir
    colunas_disponiveis = df.columns.tolist()
    colunas_padrao = ['id_obra', 'nome_obra', 'regiao', 'status', 'valor_contrato', 
                      'percentual_execucao', 'status_semaforo']
    colunas_exibir = [col for col in colunas_padrao if col in colunas_disponiveis]
    
    # Formatação da tabela
    df_display = df[colunas_exibir].copy()
    if 'valor_contrato' in df_display.columns:
        df_display['valor_contrato'] = df_display['valor_contrato'].apply(lambda x: f"R$ {x:,.2f}")
    if 'percentual_execucao' in df_display.columns:
        df_display['percentual_execucao'] = df_display['percentual_execucao'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )
    
    # Download dos dados
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="obras_der_mg.csv",
        mime="text/csv"
    )

def page_mapa(df):
    """Página 3: Mapa de Obras"""
    st.title("🗺️ Mapa de Obras")
    st.markdown("---")
    
    # Filtra obras com geolocalização
    df_geo = df[df['tem_geolocalizacao'] == True].copy()
    
    if len(df_geo) == 0:
        st.warning("⚠️ Nenhuma obra com geolocalização disponível nos filtros selecionados.")
        return
    
    st.info(f"📍 Exibindo {len(df_geo)} obras com geolocalização")
    
    # Cria mapa centrado em MG
    m = folium.Map(
        location=[-18.5, -44.0],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Cores por status semáforo
    cores_semaforo = {
        'verde': 'green',
        'amarelo': 'orange',
        'vermelho': 'red',
        'azul': 'blue'
    }
    
    # Adiciona marcadores
    for idx, row in df_geo.iterrows():
        cor = cores_semaforo.get(row['status_semaforo'], 'gray')
        
        popup_html = f"""
        <div style="width: 250px;">
            <h4>{row['nome_obra']}</h4>
            <p><b>Região:</b> {row['regiao']}</p>
            <p><b>Status:</b> {row['status']}</p>
            <p><b>Valor:</b> R$ {row['valor_contrato']:,.2f}</p>
            <p><b>Execução:</b> {row['percentual_execucao']:.1f}%</p>
            <p><b>Tipo:</b> {row['tipo_obra']}</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            popup=folium.Popup(popup_html, max_width=300),
            color=cor,
            fill=True,
            fillColor=cor,
            fillOpacity=0.7,
            weight=2
        ).add_to(m)
    
    # Legenda
    st.markdown("""
    **Legenda:**
    - 🟢 Verde: Obra no prazo
    - 🟡 Amarelo: Atraso moderado
    - 🔴 Vermelho: Atraso grave ou paralisada
    - 🔵 Azul: Em licitação
    """)
    
    # Exibe mapa
    folium_static(m, width=1200, height=600)
    
    # Estatísticas do mapa
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Obras no Mapa", len(df_geo))
    
    with col2:
        valor_total_geo = df_geo['valor_contrato'].sum()
        st.metric("Valor Total", f"R$ {valor_total_geo/1e6:.1f}M")
    
    with col3:
        exec_media_geo = df_geo['percentual_execucao'].mean()
        st.metric("Execução Média", f"{exec_media_geo:.1f}%")

def main():
    """Função principal do dashboard"""
    
    # Carrega dados
    df = load_data()
    metadata = load_metadata()
    
    # Sidebar
    st.sidebar.title("🚧 DER-MG Dashboard")
    st.sidebar.markdown("---")
    
    # Aplica filtros
    df_filtrado = apply_filters(df)
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 **{len(df_filtrado)}** obras selecionadas de **{len(df)}** totais")
    
    # Menu de navegação
    st.sidebar.markdown("---")
    pagina = st.sidebar.radio(
        "Navegação",
        ["📊 Visão Geral", "📈 Análises", "🗺️ Mapa"]
    )
    
    # Renderiza página selecionada
    if pagina == "📊 Visão Geral":
        page_visao_geral(df_filtrado)
    elif pagina == "📈 Análises":
        page_analises(df_filtrado)
    elif pagina == "🗺️ Mapa":
        page_mapa(df_filtrado)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Sobre")
    st.sidebar.markdown("""
    Dashboard de obras públicas do DER-MG.
    
    **Fonte de dados:** Portal da Transparência MG
    
    **Desenvolvido por:** Cristiane
    """)
    
    if metadata:
        st.sidebar.markdown(f"**Última atualização:** {metadata.get('data_processamento', 'N/A')[:10]}")

if __name__ == "__main__":
    main()

# Made with Bob
