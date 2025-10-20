import pandas as pd
import sqlite3

def InversionEvolucionAnual(dbName):
    try:
        conn = sqlite3.connect(dbName)
        query = '''
            SELECT f.año,
                   SUM(f.FNCE) AS total_FNCE,
                   SUM(f.GEE_final) AS total_GEE
            FROM FactInversiones f
            GROUP BY f.año
            ORDER BY f.año;
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)


def DescuentoPromedio(dbName):
    try:
        conn = sqlite3.connect(dbName)
        query = '''
            SELECT AVG(f.Descuento_FNCE) AS promedio_descuento_FNCE,
                   AVG(f.Descuento_GEE) AS promedio_descuento_GEE
            FROM FactInversiones f;
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)


def RankingRegiones(dbName):
    try:
        conn = sqlite3.connect(dbName)
        query = '''
            SELECT f.region,
                   SUM(f.FNCE) AS total_FNCE,
                   SUM(f.GEE_final) AS total_GEE,
                   (SUM(f.FNCE) + SUM(f.GEE_final)) AS total_inversion
            FROM FactInversiones f
            GROUP BY f.region
            ORDER BY total_inversion DESC;
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)



def IndiceEficienciaEnergetica(dbName):
    try:
        conn = sqlite3.connect(dbName)
        query = '''
            SELECT f.region,
                   f.año,
                   SUM(f.FNCE) AS total_FNCE,
                   SUM(f.GEE_final) AS total_GEE,
                   CASE 
                       WHEN SUM(f.GEE_final) = 0 THEN NULL
                       ELSE ROUND(SUM(f.FNCE) * 1.0 / SUM(f.GEE_final), 2)
                   END AS indice_eficiencia
            FROM FactInversiones f
            GROUP BY f.region, f.año
            ORDER BY f.año, indice_eficiencia DESC;
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)


def DescuentoPromedioRegion(dbName):
    try:
        conn = sqlite3.connect(dbName)
        query = '''
            SELECT 
                f.region,
                SUM(f.suma_EFA) AS total_descuento_FNCE,
                SUM(f.suma_GEE) AS total_descuento_GEE,
                (SUM(f.suma_EFA) + SUM(f.suma_GEE)) AS total_descuento
            FROM FactInversiones f
            GROUP BY f.region
            ORDER BY total_descuento DESC;
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)


