"""
Módulo de carga de dados processados
Salva dados em formatos otimizados para o dashboard
Autor: Cristiane
Data: 2026-05-15
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json

class DERMGLoader:
    """Carregador de dados processados do DER-MG"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
    def save_to_csv(self, df, filename="obras_processadas.csv"):
        """
        Salva DataFrame em CSV com encoding UTF-8
        """
        output_path = self.processed_dir / filename
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"💾 CSV salvo: {output_path}")
        return output_path
    
    def save_to_parquet(self, df, filename="obras_processadas.parquet"):
        """
        Salva DataFrame em Parquet (formato otimizado)
        """
        output_path = self.processed_dir / filename
        df.to_parquet(output_path, index=False, engine='pyarrow', compression='snappy')
        print(f"💾 Parquet salvo: {output_path}")
        return output_path
    
    def save_metadata(self, df):
        """
        Salva metadados sobre o dataset processado
        """
        metadata = {
            'data_processamento': datetime.now().isoformat(),
            'total_registros': len(df),
            'total_colunas': len(df.columns),
            'colunas': list(df.columns),
            'tipos_dados': df.dtypes.astype(str).to_dict(),
            'estatisticas': {
                'total_obras': len(df),
                'obras_em_andamento': len(df[df['status'] == 'Em andamento']),
                'obras_concluidas': len(df[df['status'] == 'Concluída']),
                'obras_paralisadas': len(df[df['status'] == 'Paralisada']),
                'valor_total_contratos': float(df['valor_contrato'].sum()),
                'valor_medio_contrato': float(df['valor_contrato'].mean()),
                'percentual_execucao_medio': float(df['percentual_execucao'].mean()),
                'regioes_unicas': int(df['regiao'].nunique()),
                'tipos_obra_unicos': int(df['tipo_obra'].nunique()),
            },
            'qualidade_dados': {
                'dados_completos': int(df['dados_completos'].sum()),
                'percentual_completos': float(df['dados_completos'].mean() * 100),
                'com_geolocalizacao': int(df['tem_geolocalizacao'].sum()),
                'percentual_geolocalizacao': float(df['tem_geolocalizacao'].mean() * 100),
            },
            'distribuicao_status_semaforo': df['status_semaforo'].value_counts().to_dict()
        }
        
        metadata_path = self.processed_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Metadados salvos: {metadata_path}")
        return metadata_path
    
    def create_summary_tables(self, df):
        """
        Cria tabelas agregadas para análises rápidas
        """
        print("📊 Criando tabelas agregadas...")
        
        # 1. Agregação por região
        por_regiao = df.groupby('regiao').agg({
            'id_obra': 'count',
            'valor_contrato': ['sum', 'mean'],
            'percentual_execucao': 'mean'
        }).round(2)
        por_regiao.columns = ['total_obras', 'valor_total', 'valor_medio', 'perc_exec_medio']
        por_regiao.to_csv(self.processed_dir / "agregado_por_regiao.csv")
        
        # 2. Agregação por status
        por_status = df.groupby('status').agg({
            'id_obra': 'count',
            'valor_contrato': 'sum',
            'percentual_execucao': 'mean'
        }).round(2)
        por_status.columns = ['total_obras', 'valor_total', 'perc_exec_medio']
        por_status.to_csv(self.processed_dir / "agregado_por_status.csv")
        
        # 3. Agregação por tipo de obra
        por_tipo = df.groupby('tipo_obra').agg({
            'id_obra': 'count',
            'valor_contrato': ['sum', 'mean']
        }).round(2)
        por_tipo.columns = ['total_obras', 'valor_total', 'valor_medio']
        por_tipo.to_csv(self.processed_dir / "agregado_por_tipo.csv")
        
        # 4. Top 10 obras por valor
        top_obras = df.nlargest(10, 'valor_contrato')[
            ['id_obra', 'nome_obra', 'regiao', 'valor_contrato', 'percentual_execucao', 'status']
        ]
        top_obras.to_csv(self.processed_dir / "top_10_obras.csv", index=False)
        
        print("   ✅ Tabelas agregadas criadas")
    
    def generate_data_quality_report(self, df):
        """
        Gera relatório de qualidade dos dados
        """
        report = []
        report.append("=" * 60)
        report.append("RELATÓRIO DE QUALIDADE DOS DADOS")
        report.append("=" * 60)
        report.append(f"\nData: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total de registros: {len(df)}")
        report.append(f"Total de colunas: {len(df.columns)}")
        
        report.append("\n📊 COMPLETUDE DOS DADOS:")
        report.append(f"   Registros completos: {df['dados_completos'].sum()} ({df['dados_completos'].mean()*100:.1f}%)")
        report.append(f"   Com geolocalização: {df['tem_geolocalizacao'].sum()} ({df['tem_geolocalizacao'].mean()*100:.1f}%)")
        
        report.append("\n🚦 DISTRIBUIÇÃO STATUS SEMÁFORO:")
        for status, count in df['status_semaforo'].value_counts().items():
            report.append(f"   {status}: {count} ({count/len(df)*100:.1f}%)")
        
        report.append("\n💰 VALORES FINANCEIROS:")
        report.append(f"   Valor total: R$ {df['valor_contrato'].sum():,.2f}")
        report.append(f"   Valor médio: R$ {df['valor_contrato'].mean():,.2f}")
        report.append(f"   Valor mínimo: R$ {df['valor_contrato'].min():,.2f}")
        report.append(f"   Valor máximo: R$ {df['valor_contrato'].max():,.2f}")
        
        report.append("\n📈 EXECUÇÃO:")
        report.append(f"   Execução média: {df['percentual_execucao'].mean():.1f}%")
        report.append(f"   Obras 100% executadas: {len(df[df['percentual_execucao'] == 100])}")
        report.append(f"   Obras sem execução: {len(df[df['percentual_execucao'] == 0])}")
        
        report.append("\n🗺️  DISTRIBUIÇÃO GEOGRÁFICA:")
        report.append(f"   Total de regiões: {df['regiao'].nunique()}")
        report.append("   Top 5 regiões:")
        for regiao, count in df['regiao'].value_counts().head().items():
            report.append(f"      {regiao}: {count} obras")
        
        report_text = "\n".join(report)
        
        # Salva relatório
        report_path = self.processed_dir / "quality_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"📄 Relatório de qualidade salvo: {report_path}")
        print("\n" + report_text)
        
        return report_path
    
    def load(self, df):
        """
        Método principal de carga
        Salva dados em múltiplos formatos e gera relatórios
        """
        print("=" * 60)
        print("💾 INICIANDO CARGA DE DADOS PROCESSADOS")
        print("=" * 60)
        
        # Salva em diferentes formatos
        csv_path = self.save_to_csv(df)
        parquet_path = self.save_to_parquet(df)
        
        # Salva metadados
        metadata_path = self.save_metadata(df)
        
        # Cria tabelas agregadas
        self.create_summary_tables(df)
        
        # Gera relatório de qualidade
        report_path = self.generate_data_quality_report(df)
        
        print("\n✅ CARGA CONCLUÍDA COM SUCESSO!")
        print(f"\n📁 Arquivos gerados em: {self.processed_dir}")
        print(f"   - {csv_path.name}")
        print(f"   - {parquet_path.name}")
        print(f"   - {metadata_path.name}")
        print(f"   - {report_path.name}")
        print("   - agregado_por_regiao.csv")
        print("   - agregado_por_status.csv")
        print("   - agregado_por_tipo.csv")
        print("   - top_10_obras.csv")
        
        return {
            'csv': csv_path,
            'parquet': parquet_path,
            'metadata': metadata_path,
            'report': report_path
        }

def main():
    """Função principal para execução standalone"""
    from transform import DERMGTransformer
    
    # Transforma dados primeiro
    transformer = DERMGTransformer()
    df = transformer.transform()
    
    # Carrega dados processados
    loader = DERMGLoader()
    paths = loader.load(df)
    
    print("\n✅ Pipeline de carga concluído!")
    return paths

if __name__ == "__main__":
    main()

# Made with Bob
