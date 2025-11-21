import pandas as pd
import sqlite3

def load_dw(conn, df_fact):
    cursor = conn.cursor()

    # Eliminar tablas previas
    cursor.execute('DROP TABLE IF EXISTS DimEmpresa')
    cursor.execute('DROP TABLE IF EXISTS DimRegion')
    cursor.execute('DROP TABLE IF EXISTS DimAño')
    cursor.execute('DROP TABLE IF EXISTS DimTipoInversion')
    cursor.execute('DROP TABLE IF EXISTS FactInversiones')

    # Crear tablas de dimensiones
    cursor.execute('''
    CREATE TABLE DimEmpresa (
        id_fuente REAL PRIMARY KEY
    )
    ''')
    cursor.execute('''
    CREATE TABLE DimRegion (
        region TEXT PRIMARY KEY
    )
    ''')
    cursor.execute('''
    CREATE TABLE DimAño (
        año INTEGER PRIMARY KEY
    )
    ''')
    cursor.execute('''
    CREATE TABLE DimTipoInversion (
        tipo_inversion TEXT PRIMARY KEY
    )
    ''')

    # Insertar datos en dimensiones
    df_fact[['id_fuente']].drop_duplicates().to_sql('DimEmpresa', conn, if_exists='append', index=False)
    df_fact[['region']].drop_duplicates().to_sql('DimRegion', conn, if_exists='append', index=False)
    df_fact[['año']].drop_duplicates().to_sql('DimAño', conn, if_exists='append', index=False)

    # Lista fija de tipos de inversión válidos
    tipos_validos = [
        'inv tierras y terrenos EFA',
        'inv maquinaria y equipo EFA',
        'inv construcciones y edificaciones EFA',
        'materiales y suministros EFA',
        'pequeñas herramientas EFA',
        'mantenimiento de equipos EFA',
        'medición, control y análisis EFA',
        'inv maquinaria y equipo (GEE)',
        'inv construcciones y edificaciones (GEE)',
        'materiales y suministros (GEE)',
        'pequeñas herramientas (GEE)',
        'mantenimiento de equipos (GEE)',
        'medición, control y análisis (GEE)'
    ]
    df_tipo = pd.DataFrame({'tipo_inversion': tipos_validos})
    df_tipo.to_sql('DimTipoInversion', conn, if_exists='replace', index=False)

    # Crear tabla de hechos
    cursor.execute('''
    CREATE TABLE FactInversiones (
        id_fuente INTEGER,
        region INTEGER,
        año INTEGER,
        FNCE REAL,
        GEE_final REAL,
        Descuento_FNCE REAL,
        Descuento_GEE REAL,
        suma_EFA REAL,
        suma_GEE REAL,
        tipo_inversion TEXT,
        porcentaje_inversion REAL,
        Sugerencia TEXT
    );
    ''')

    # Filtrar NaN para integridad
    df_fact = df_fact.dropna(subset=['id_fuente', 'region', 'año', 'tipo_inversion'])

    # Asegurar tipo correcto
    df_fact['suma_EFA'] = df_fact['suma_EFA'].astype(float)
    df_fact['suma_GEE'] = df_fact['suma_GEE'].astype(float)

    # Insertar datos con orden exacto de la tabla
    df_fact[[
        'id_fuente','region','año','FNCE','GEE_final','Descuento_FNCE','Descuento_GEE',
        'suma_EFA','suma_GEE','tipo_inversion','porcentaje_inversion','Sugerencia'
    ]].to_sql('FactInversiones', conn, if_exists='append', index=False)

    # Commit
    conn.commit()
    print("DW cargado correctamente. Las tablas han sido actualizadas.")
    #print(df_fact[['suma_EFA','suma_GEE']].head())
