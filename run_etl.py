#!/usr/bin/env python3
"""
Script para executar o pipeline ETL completo
Autor: Cristiane
Data: 2026-05-15
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from etl.extract import DERMGExtractor
from etl.transform import DERMGTransformer
from etl.load import DERMGLoader
from datetime import datetime

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def main():
    """Executa o pipeline ETL completo"""
    
    print_header("🚀 PIPELINE ETL - OBRAS PÚBLICAS DER-MG")
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # ETAPA 1: EXTRAÇÃO
        print_header("📥 ETAPA 1/3: EXTRAÇÃO DE DADOS")
        extractor = DERMGExtractor()
        df_raw = extractor.extract()
        
        if df_raw is None or df_raw.empty:
            print("❌ Erro: Nenhum dado foi extraído")
            return 1
        
        print(f"\n✅ Extração concluída: {len(df_raw)} registros")
        
        # ETAPA 2: TRANSFORMAÇÃO
        print_header("🔄 ETAPA 2/3: TRANSFORMAÇÃO DE DADOS")
        transformer = DERMGTransformer()
        df_transformed = transformer.transform()
        
        if df_transformed is None or df_transformed.empty:
            print("❌ Erro: Falha na transformação dos dados")
            return 1
        
        print(f"\n✅ Transformação concluída: {len(df_transformed)} registros processados")
        
        # ETAPA 3: CARGA
        print_header("💾 ETAPA 3/3: CARGA DE DADOS")
        loader = DERMGLoader()
        paths = loader.load(df_transformed)
        
        print(f"\n✅ Carga concluída com sucesso!")
        
        # RESUMO FINAL
        print_header("📊 RESUMO DO PIPELINE")
        print(f"✅ Pipeline executado com sucesso!")
        print(f"⏱️  Tempo de execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Dados salvos em: data/processed/")
        print(f"📈 Total de registros: {len(df_transformed)}")
        print(f"💰 Valor total: R$ {df_transformed['valor_contrato'].sum():,.2f}")
        print(f"🗺️  Regiões: {df_transformed['regiao'].nunique()}")
        print(f"🏗️  Tipos de obra: {df_transformed['tipo_obra'].nunique()}")
        
        print("\n" + "=" * 70)
        print("🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print("\n💡 Próximo passo: Execute o dashboard com:")
        print("   streamlit run dashboard/app.py\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERRO NO PIPELINE: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

# Made with Bob
