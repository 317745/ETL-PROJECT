import pandas as pd
import sqlite3

# ------------------------------
# FUNCIONES KPI PARA DASH
# ------------------------------

def InversionPorRegionFNCE(dbName):
    """Inversión en FNCE por región (usando nombres)"""
    conn = sqlite3.connect(dbName)
    try:
        df = pd.read_sql_query('''
            SELECT r.name AS region,
                   SUM(f.FNCE) AS total_FNCE
            FROM FactInversiones f
            JOIN DimRegion d ON f.region = d.region
            JOIN regions r ON d.region = r.rowid
            GROUP BY r.name
            ORDER BY r.name;
        ''', conn)
        return df
    finally:
        conn.close()


def InversionPorRegionGEE(dbName):
    """Inversión en GEE por región (usando nombres)"""
    conn = sqlite3.connect(dbName)
    try:
        df = pd.read_sql_query('''
            SELECT r.name AS region,
                   SUM(f.GEE_final) AS total_GEE
            FROM FactInversiones f
            JOIN DimRegion d ON f.region = d.region
            JOIN regions r ON d.region = r.rowid
            GROUP BY r.name
            ORDER BY r.name;
        ''', conn)
        return df
    finally:
        conn.close()


def EvolucionAnualPorRegion(dbName):
    """Evolución anual de inversión FNCE y GEE por región"""
    conn = sqlite3.connect(dbName)
    try:
        df = pd.read_sql_query('''
            SELECT r.name AS region,
                   f.año,
                   SUM(f.FNCE) AS total_FNCE,
                   SUM(f.GEE_final) AS total_GEE
            FROM FactInversiones f
            JOIN DimRegion d ON f.region = d.region
            JOIN regions r ON d.region = r.rowid
            GROUP BY r.name, f.año
            ORDER BY r.name, f.año;
        ''', conn)
        return df
    finally:
        conn.close()

def TipoInversionPredominantePorRegion(dbName):
    """Tipo de inversión más frecuente por región"""
    conn = sqlite3.connect(dbName)
    try:
        # Traemos región y tipo de inversión
        df = pd.read_sql_query('''
            SELECT r.name AS region,
                   f.tipo_inversion
            FROM FactInversiones f
            JOIN DimRegion d ON f.region = d.region
            JOIN regions r ON d.region = r.rowid
        ''', conn)

       
        df_freq = df.groupby(['region', 'tipo_inversion']).size().reset_index(name='frecuencia')

        # tipo de inversión con mayor frecuencia por región
        df_top_tipo = df_freq.loc[df_freq.groupby('region')['frecuencia'].idxmax()].reset_index(drop=True)

        return df_top_tipo

    finally:
        conn.close()