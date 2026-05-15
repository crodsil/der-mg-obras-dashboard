"""
Módulo de transformação de dados de obras públicas do DER-MG
Aplica limpeza, normalização e enriquecimento dos dados
Autor: Cristiane
Data: 2026-05-15
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import re
import unicodedata

class DERMGTransformer:
    """Transformador de dados de obras públicas do DER-MG"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        
    def normalize_column_names(self, df):
        """
        Normaliza nomes de colunas para snake_case sem acentos
        """
        print("🔧 Normalizando nomes de colunas...")
        
        def to_snake_case(text):
            # Remove acentos
            text = unicodedata.normalize('NFKD', text)
            text = text.encode('ASCII', 'ignore').decode('ASCII')
            # Converte para snake_case
            text = re.sub(r'[^\w\s]', '', text)
            text = re.sub(r'\s+', '_', text)
            return text.lower()
        
        df.columns = [to_snake_case(col) for col in df.columns]
        return df
    
    def clean_monetary_values(self, df):
        """
        Limpa e converte valores monetários para float
        """
        print("💰 Processando valores monetários...")
        
        if 'valor_contrato' in df.columns:
            # Se já for numérico, mantém
            if df['valor_contrato'].dtype in ['float64', 'int64']:
                return df
            
            # Se for string, limpa e converte
            df['valor_contrato'] = df['valor_contrato'].astype(str)
            df['valor_contrato'] = df['valor_contrato'].str.replace('R$', '', regex=False)
            df['valor_contrato'] = df['valor_contrato'].str.replace('.', '', regex=False)
            df['valor_contrato'] = df['valor_contrato'].str.replace(',', '.', regex=False)
            df['valor_contrato'] = pd.to_numeric(df['valor_contrato'], errors='coerce')
        
        return df
    
    def convert_dates(self, df):
        """
        Converte colunas de data para datetime
        """
        print("📅 Convertendo datas...")
        
        date_columns = ['data_inicio', 'data_extracao']
        
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    
    def calculate_derived_fields(self, df):
        """
        Calcula campos derivados importantes
        """
        print("🧮 Calculando campos derivados...")
        
        # 1. Data prevista de conclusão
        if 'data_inicio' in df.columns and 'prazo_meses' in df.columns:
            df['data_prevista_conclusao'] = df.apply(
                lambda row: row['data_inicio'] + timedelta(days=row['prazo_meses']*30) 
                if pd.notna(row['data_inicio']) and pd.notna(row['prazo_meses']) 
                else pd.NaT,
                axis=1
            )
        
        # 2. Dias desde o início
        if 'data_inicio' in df.columns:
            hoje = pd.Timestamp.now()
            df['dias_desde_inicio'] = (hoje - df['data_inicio']).dt.days
            df['dias_desde_inicio'] = df['dias_desde_inicio'].fillna(0).astype(int)
        
        # 3. Status semáforo (verde/amarelo/vermelho)
        df['status_semaforo'] = df.apply(self._calcular_status_semaforo, axis=1)
        
        # 4. Valor executado
        if 'valor_contrato' in df.columns and 'percentual_execucao' in df.columns:
            df['valor_executado'] = df['valor_contrato'] * (df['percentual_execucao'] / 100)
        
        # 5. Categoria de valor
        if 'valor_contrato' in df.columns:
            df['categoria_valor'] = pd.cut(
                df['valor_contrato'],
                bins=[0, 1000000, 5000000, 10000000, float('inf')],
                labels=['Pequeno', 'Médio', 'Grande', 'Muito Grande']
            )
        
        return df
    
    def _calcular_status_semaforo(self, row):
        """
        Calcula status semáforo baseado em execução vs prazo
        Verde: obra no prazo
        Amarelo: obra com atraso leve
        Vermelho: obra com atraso grave ou paralisada
        """
        if row['status'] == 'Paralisada':
            return 'vermelho'
        
        if row['status'] == 'Concluída':
            return 'verde'
        
        if row['status'] == 'Em licitação':
            return 'azul'
        
        # Para obras em andamento
        if pd.notna(row.get('percentual_execucao')) and pd.notna(row.get('dias_desde_inicio')):
            perc_exec = row['percentual_execucao']
            dias_decorridos = row['dias_desde_inicio']
            prazo_total_dias = row.get('prazo_meses', 12) * 30
            
            if prazo_total_dias > 0:
                perc_tempo_decorrido = (dias_decorridos / prazo_total_dias) * 100
                diferenca = perc_exec - perc_tempo_decorrido
                
                if diferenca >= -10:  # Execução acompanha ou está adiantada
                    return 'verde'
                elif diferenca >= -25:  # Atraso moderado
                    return 'amarelo'
                else:  # Atraso grave
                    return 'vermelho'
        
        return 'amarelo'  # Default
    
    def handle_missing_values(self, df):
        """
        Trata valores nulos com estratégia documentada
        """
        print("🔍 Tratando valores nulos...")
        
        # Estratégias por coluna
        estrategias = {
            'percentual_execucao': 0,  # Obras sem execução = 0%
            'empresa_contratada': 'Não informado',
            'latitude': None,  # Mantém nulo se não houver coordenadas
            'longitude': None,
            'prazo_meses': 12  # Prazo padrão de 12 meses
        }
        
        for col, valor in estrategias.items():
            if col in df.columns:
                if valor is not None:
                    df[col] = df[col].fillna(valor)
        
        # Log de nulos restantes
        nulos = df.isnull().sum()
        if nulos.sum() > 0:
            print("\n⚠️  Valores nulos restantes:")
            print(nulos[nulos > 0])
        
        return df
    
    def add_quality_flags(self, df):
        """
        Adiciona flags de qualidade dos dados
        """
        print("🏷️  Adicionando flags de qualidade...")
        
        # Flag: dados completos
        df['dados_completos'] = ~df[['valor_contrato', 'data_inicio', 'percentual_execucao']].isnull().any(axis=1)
        
        # Flag: tem geolocalização
        df['tem_geolocalizacao'] = ~df[['latitude', 'longitude']].isnull().any(axis=1)
        
        # Flag: obra recente (últimos 2 anos)
        if 'data_inicio' in df.columns:
            dois_anos_atras = pd.Timestamp.now() - timedelta(days=730)
            df['obra_recente'] = df['data_inicio'] >= dois_anos_atras
        
        return df
    
    def transform(self, input_path=None):
        """
        Método principal de transformação
        """
        print("=" * 60)
        print("🔄 INICIANDO TRANSFORMAÇÃO DE DADOS")
        print("=" * 60)
        
        # Carrega dados brutos
        if input_path is None:
            input_path = self.data_dir / "raw_obras.csv"
        
        print(f"\n📂 Carregando dados de: {input_path}")
        df = pd.read_csv(input_path)
        print(f"   Registros carregados: {len(df)}")
        
        # Aplica transformações
        df = self.normalize_column_names(df)
        df = self.clean_monetary_values(df)
        df = self.convert_dates(df)
        df = self.calculate_derived_fields(df)
        df = self.handle_missing_values(df)
        df = self.add_quality_flags(df)
        
        # Estatísticas finais
        print("\n📊 ESTATÍSTICAS PÓS-TRANSFORMAÇÃO:")
        print(f"   Total de registros: {len(df)}")
        print(f"   Colunas: {len(df.columns)}")
        print(f"   Dados completos: {df['dados_completos'].sum()} ({df['dados_completos'].mean()*100:.1f}%)")
        print(f"   Com geolocalização: {df['tem_geolocalizacao'].sum()} ({df['tem_geolocalizacao'].mean()*100:.1f}%)")
        
        print("\n   Status semáforo:")
        print(df['status_semaforo'].value_counts().to_string())
        
        return df

def main():
    """Função principal para execução standalone"""
    transformer = DERMGTransformer()
    df = transformer.transform()
    print("\n✅ Transformação concluída com sucesso!")
    return df

if __name__ == "__main__":
    main()

# Made with Bob
