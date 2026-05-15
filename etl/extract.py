"""
Módulo de extração de dados de obras públicas do DER-MG
Autor: Cristiane
Data: 2026-05-15
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import time
import random
from pathlib import Path

class DERMGExtractor:
    """Extrator de dados de obras públicas do DER-MG"""
    
    def __init__(self):
        self.base_url = "https://www.transparencia.mg.gov.br"
        self.der_url = "https://www.der.mg.gov.br/transparencia/obras-publicas"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
    def extract_from_web(self):
        """
        Tenta extrair dados do site oficial
        Retorna DataFrame ou None se falhar
        """
        try:
            print("🔍 Tentando extrair dados do site oficial...")
            response = requests.get(self.der_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Aqui você implementaria a lógica específica de scraping
                # baseado na estrutura real do site
                print("✅ Conexão estabelecida com sucesso")
                return self._parse_html(soup)
            else:
                print(f"⚠️  Status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao acessar site: {str(e)}")
            return None
    
    def _parse_html(self, soup):
        """Parse do HTML para extrair dados estruturados"""
        # Implementação específica baseada na estrutura do site
        # Por enquanto, retorna None para usar dados simulados
        return None
    
    def generate_sample_data(self):
        """
        Gera dados simulados realistas para demonstração
        Estrutura baseada em dados típicos de obras públicas
        """
        print("📊 Gerando dados simulados realistas...")
        
        # Regiões do DER-MG
        regioes = [
            'Belo Horizonte', 'Juiz de Fora', 'Montes Claros', 
            'Uberlândia', 'Governador Valadares', 'Varginha',
            'Uberaba', 'Patos de Minas', 'Teófilo Otoni'
        ]
        
        # Status possíveis
        status_opcoes = ['Em andamento', 'Concluída', 'Paralisada', 'Em licitação']
        
        # Tipos de obra
        tipos_obra = [
            'Pavimentação', 'Restauração', 'Duplicação', 
            'Ponte', 'Viaduto', 'Sinalização', 'Drenagem'
        ]
        
        # Gerar 150 obras simuladas
        n_obras = 150
        data = []
        
        for i in range(1, n_obras + 1):
            # Dados básicos
            regiao = random.choice(regioes)
            tipo = random.choice(tipos_obra)
            status = random.choice(status_opcoes)
            
            # Valores financeiros
            valor_contrato = random.uniform(500000, 15000000)
            percentual_execucao = random.uniform(0, 100) if status != 'Em licitação' else 0
            
            # Datas
            ano_inicio = random.randint(2020, 2024)
            mes_inicio = random.randint(1, 12)
            data_inicio = f"{ano_inicio}-{mes_inicio:02d}-{random.randint(1, 28):02d}"
            
            # Prazo em meses
            prazo_meses = random.randint(6, 36)
            
            # Rodovia
            rodovia = f"MG-{random.randint(10, 999):03d}"
            
            # Coordenadas aproximadas de MG
            latitude = random.uniform(-22.5, -15.0)
            longitude = random.uniform(-51.0, -40.0)
            
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
                'data_extracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            data.append(obra)
        
        df = pd.DataFrame(data)
        print(f"✅ {len(df)} obras geradas com sucesso")
        return df
    
    def extract(self):
        """
        Método principal de extração
        Tenta web scraping, se falhar usa dados simulados
        """
        print("=" * 60)
        print("🚀 INICIANDO EXTRAÇÃO DE DADOS DER-MG")
        print("=" * 60)
        
        # Tenta extrair do site real
        df = self.extract_from_web()
        
        # Se falhar, usa dados simulados
        if df is None or df.empty:
            print("\n⚠️  Usando dados simulados para demonstração")
            df = self.generate_sample_data()
        
        # Salva dados brutos
        raw_path = self.data_dir / "raw_obras.csv"
        df.to_csv(raw_path, index=False, encoding='utf-8-sig')
        print(f"\n💾 Dados salvos em: {raw_path}")
        
        # Estatísticas
        print("\n📈 ESTATÍSTICAS DA EXTRAÇÃO:")
        print(f"   Total de obras: {len(df)}")
        print(f"   Regiões: {df['regiao'].nunique()}")
        print(f"   Tipos de obra: {df['tipo_obra'].nunique()}")
        print(f"   Valor total: R$ {df['valor_contrato'].sum():,.2f}")
        
        return df

def main():
    """Função principal para execução standalone"""
    extractor = DERMGExtractor()
    df = extractor.extract()
    print("\n✅ Extração concluída com sucesso!")
    return df

if __name__ == "__main__":
    main()

# Made with Bob
