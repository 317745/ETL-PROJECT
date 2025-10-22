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
