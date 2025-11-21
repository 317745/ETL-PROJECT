import sqlite3
import pandas as pd

DB_PATH = "applications.db"

def get_tables(conn):
    return pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table';", conn
    )['name'].tolist()

def load_table(conn, table_name):
    return pd.read_sql_query(f"SELECT * FROM {table_name};", conn)

def validate_nulls(df):
    return df.isnull().sum().reset_index().rename(
        columns={'index': 'column', 0: 'null_count'}
    )

def validate_duplicates(df):
    return df.duplicated().sum()

def validate_foreign_keys(conn, fact_table, fk_column, dim_table, dim_key):
    query = f"""
        SELECT f.{fk_column}
        FROM {fact_table} f
        LEFT JOIN {dim_table} d
        ON f.{fk_column} = d.{dim_key}
        WHERE d.{dim_key} IS NULL
        AND f.{fk_column} IS NOT NULL;
    """
    return pd.read_sql_query(query, conn)

def main():

    print("\n========== VALIDACIÓN DE CALIDAD DE DATOS ==========\n")

    conn = sqlite3.connect(DB_PATH)
    tables = get_tables(conn)

    print(f"Tablas encontradas: {tables}\n")

    for table in tables:
        print(f"\n📌 ----- Analizando tabla: {table} -----")

        df = load_table(conn, table)

        print(f"Registros: {len(df)}   Columnas: {len(df.columns)}")

        # 1. NULOS
        print("\n🔸 Nulos por columna:")
        print(validate_nulls(df))

        # 2. DUPLICADOS
        dups = validate_duplicates(df)
        print(f"\n🔸 Filas duplicadas: {dups}")

        # 3. TIPOS DE DATOS
        print("\n🔸 Tipos detectados:")
        print(df.dtypes)

        # 4. VALORES ÚNICOS RAROS (categorías)
        print("\n🔸 Valores únicos por columna:")
        for col in df.columns:
            uniques = df[col].nunique()
            print(f"   {col}: {uniques}")

   
if __name__ == "__main__":
    main()
