import pandas as pd
from kpi import (
    InversionEvolucionAnual,
    DescuentoPromedio,
    RankingRegiones,
    IndiceEficienciaEnergetica,
    RetornoEstimadoInversion,
)

DB_NAME = "applications.db"

def main():
    # KPI #1
    df_inversion = InversionEvolucionAnual(DB_NAME)
    print("KPI #1 - Evolución anual de la inversión (FNCE y GEE)")
    print(df_inversion if isinstance(df_inversion, str) else df_inversion.to_string(index=False))
    print("-" * 80)

    # KPI #2
    df_descuento = DescuentoPromedio(DB_NAME)
    print("KPI #2 - Descuento promedio aplicado (FNCE y GEE)")
    print(df_descuento if isinstance(df_descuento, str) else df_descuento.to_string(index=False))
    print("-" * 80)

    # KPI #3
    df_ranking = RankingRegiones(DB_NAME)
    print("KPI #3 - Ranking de regiones por nivel de inversión FNCE/GEE")
    print(df_ranking if isinstance(df_ranking, str) else df_ranking.to_string(index=False))
    print("-" * 80)

    # KPI #4
    df_indice = IndiceEficienciaEnergetica(DB_NAME)
    print("KPI #4 - Índice de Eficiencia Energética (FNCE / GEE)")
    print(df_indice if isinstance(df_indice, str) else df_indice.to_string(index=False))
    print("-" * 80)


    # KPI #5 (si quieres mantener el retorno de inversión)
    df_retorno = RetornoEstimadoInversion(DB_NAME)
    print("KPI #5 - Retorno estimado de la inversión")
    print(df_retorno if isinstance(df_retorno, str) else df_retorno.to_string(index=False))
    print("-" * 80)


if __name__ == "__main__":
    main()
