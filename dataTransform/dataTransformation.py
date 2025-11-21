from datetime import datetime
import pandas as pd


import numpy as np



class transformation:
    def __init__(self, df):
        self.df = df
        #Limpiar columnas resecto a espacios
    
        df.columns = df.columns.str.strip()
        
        # Guardar el DataFrame limpio 
        self.df = df
        
        #print(df[['id_fuente', 'inv maquinaria y equipo (GEE)']].head())
        
    # 1. Definir si es mejor para la empresa invertir en EFA o GEE

    def FNCE_comprobation(self):
        for col in self.df.columns:
            if "EFA" in col or "GEE" in col:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
                
        self.df['suma_EFA'] = 0

        # Sumar todas las columnas que tengan "EFA" en el nombre pero no "inversión total EFA ni totales"
        excluir_efa = [
            "inversión total EFA",
            "total costos y gastos EFA",
            "total inversión y gastos EFA"]
        # Definir columnas a sumar
        efa_cols = [col for col in self.df.columns if "EFA" in col and col not in excluir_efa and "_prop" not in col]
        self.df['suma_EFA'] = self.df[efa_cols].sum(axis=1, skipna=True)


        # Si la suma coincide con inversión total EFA poner esa suma si no 0
        self.df['FNCE_aprobado'] = np.where(
            np.isclose(self.df['suma_EFA'], 
                       self.df['inversión total EFA'], rtol=1e-3),
                       self.df['suma_EFA'],
                       0 )

         # Identificar filas con error (cuando hay diferencia y no son ambos cero)
        errores = self.df[
            ~np.isclose(self.df['suma_EFA'], self.df['inversión total EFA'], rtol=1e-3) &
            ~((self.df['suma_EFA'] == 0) & (self.df['inversión total EFA'] == 0))]

        if errores.empty:
            print("El total del dataset para el total FNCE es correcto")
        else:
            pass
            #print(f"Se encontraron {len(errores)} filas con errores para el total de FNCE en los siguientes id_fuente:\n")
        # Mostrar solo las columnas clave para revisar
            #print(errores[['id_fuente','region','año', 'suma_EFA', 'inversión total EFA']].head(10).to_markdown(index=False))

        # Calcular descuento aplicado a inversión de FNCE/EFA
        self.df['Descuento_FNCE'] = self.df['suma_EFA'] * 0.5
        self.df['FNCE'] = self.df['suma_EFA'] - self.df['Descuento_FNCE']

        # Devolver la columna con descuento
        return self.df[['FNCE']]

    def GEE_comprobation(self):
        
        for col in self.df.columns:
            if "EFA" in col or "GEE" in col:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
                
        self.df['suma_GEE'] = 0

        # Sumar todas las columnas que tengan "GEE" en el nombre pero no "inversión total GEE" ni totales
        excluir_gee = [
            "inversión total (GEE)",
            "total costos y gastos (GEE)",
            "total inversión y gastos (GEE)"]
        gee_cols = [col for col in self.df.columns if "GEE" in col and col not in excluir_gee and "_prop" not in col]
        self.df['suma_GEE'] = self.df[gee_cols].sum(axis=1, skipna=True)

        # Si la suma coincide con inversión total GEE poner esa suma si no 0
        self.df['GEE_aprobado'] = np.where(
            np.isclose(self.df['suma_GEE'], 
                       self.df['inversión total (GEE)'], rtol=1e-3),
            self.df['suma_GEE'],
            0 )

        # Identificar filas con error
        errores = self.df[
            ~np.isclose(self.df['suma_GEE'], self.df['inversión total (GEE)'], rtol=1e-3) &
            ~((self.df['suma_GEE'] == 0) & (self.df['inversión total (GEE)'] == 0))]


        if errores.empty:
            print("El total del dataset para el total GEE es correcto")
        else:
            pass
            #print(f"Se encontraron {len(errores)} filas con errores para el total de GEE en los siguientes id_fuente:\n")
        # Mostrar solo las columnas clave para revisar
            #print(errores[['id_fuente','region','año','suma_GEE', 'inversión total (GEE)']].head(10).to_markdown(index=False))

        # Calcular descuento aplicado a inversión de GEE
        self.df['Descuento_GEE'] = self.df['suma_GEE'] * 0.5
        self.df['GEE'] = self.df['suma_GEE'] - self.df['Descuento_GEE']
        

        # Tomaremos como columna de certificacion ANLA a inv maquinaria y equipo (GEE),si inv maquinaria y equipo (GEE) > 0 entonces se cuenta con la certificación ANLA
        self.df['GEE_final'] = np.where(
            self.df['inv maquinaria y equipo (GEE)'] > 0,
            self.df['GEE'] * 0.75,
            self.df['GEE'])


        # Devolver la columna con descuento
        return self.df[['GEE_final']]
        
    
        
        
    # 2. Análisis de inversión por tipo de activo 
    
    def FNCE_proportion(self):
        efa_cols = [c for c in self.df.columns
                    if "EFA" in c and 
                    "total" not in c.lower() and 
                    "inversión total" not in c.lower() and
                    "costos" not in c.lower() and
                    "gastos" not in c.lower()]
        
        denom = self.df["suma_EFA"] + self.df["suma_GEE"]

        for col in efa_cols:
            self.df[col + "_prop"] = np.where(
                 denom > 0,
                 (self.df[col] / denom) * 100,
                 0)


    def GEE_proportion(self):
        gee_cols = [c for c in self.df.columns 
                   if "GEE" in c and
                   "total" not in c.lower() and
                   "inversión total" not in c.lower() and
                   "costos" not in c.lower() and
                   "gastos" not in c.lower()]
        
        denom = self.df["suma_EFA"] + self.df["suma_GEE"]

        for col in gee_cols:
            self.df[col + "_prop"] = np.where(
                 denom > 0,
                 (self.df[col] / denom) * 100,
                 0)



        
    # 3. Análisis por región
    def region_analisis(self, threshold=10):
        self.FNCE_proportion()
        self.GEE_proportion()

        # Seleccionar columnas de porcentaje
        efa_cols = [c for c in self.df.columns 
                    if 'EFA' in c 
            and "prop" not in c.lower()  
            and "suma" not in c.lower()
            and "descuento" not in c.lower()
            and "total" not in c.lower()
            and "costo" not in c.lower()
            and "gasto" not in c.lower()]
        denom = self.df["suma_EFA"] + self.df["suma_GEE"]
        for col in efa_cols:
            self.df[col + "_prop"] = np.where(denom > 0, (self.df[col] / denom) * 100, 0)
        
        gee_cols = [c for c in self.df.columns 
                    if '(GEE)' in c 
            and "prop" not in c.lower()
            and "suma" not in c.lower()
            and "descuento" not in c.lower()
            and "total" not in c.lower()
            and "costo" not in c.lower()
            and "gasto" not in c.lower()
                    ]
        denom = self.df["suma_EFA"] + self.df["suma_GEE"]
        for col in gee_cols:
            self.df[col + "_prop"] = np.where(denom > 0, (self.df[col] / denom) * 100, 0)

        # Agrupar por región y calcular promedio de cada porcentaje
        region_summary = self.df.groupby(['id_fuente', 'region'])[efa_cols + gee_cols].mean().reset_index()

        # Calcular porcentaje total de EFA y GEE por región
        region_summary['EFA_total_prop'] = region_summary[efa_cols].sum(axis=1)
        region_summary['GEE_total_prop'] = region_summary[gee_cols].sum(axis=1)

        # Lógica de sugerencia correcta
        def sugerencia_region(row):
           if row['EFA_total_prop'] == 0 and row['GEE_total_prop'] == 0:
                return "Sin inversión"
           elif row['EFA_total_prop'] < threshold:
                return "Considerar invertir en EFA"
           elif row['GEE_total_prop'] < threshold:
                return "Considerar invertir en GEE"
           else:
                return ""  

        region_summary['Sugerencia'] = region_summary.apply(sugerencia_region, axis=1)

        return region_summary
    
    def create_fact_table(self, threshold=10): 
        efa_prop_cols = [c for c in self.df.columns if c.endswith('EFA_prop')]
        gee_prop_cols = [c for c in self.df.columns if c.endswith('(GEE)_prop')]



        # Crear columnas totales por fila
        self.df['EFA_total_prop'] = self.df[efa_prop_cols].sum(axis=1)
        self.df['GEE_total_prop'] = self.df[gee_prop_cols].sum(axis=1)

        # Lógica de sugerencia
        def sugerencia_fact(row):
            if row['EFA_total_prop'] == 0 and row['GEE_total_prop'] == 0:
                return "Sin inversión"
            elif row['EFA_total_prop'] < threshold:
                return "Considerar invertir en EFA"
            elif row['GEE_total_prop'] < threshold:
                return "Considerar invertir en GEE"
            else:
                return ""  # Ninguna sugerencia si ambos >= threshold

        self.df['Sugerencia'] = self.df.apply(sugerencia_fact, axis=1)

    
   
        value_vars = [
            col for col in (efa_prop_cols + gee_prop_cols)
            if "suma" not in col.lower() and "descuento" not in col.lower() and col not in ["EFA_prop", "GEE_prop"]]

        
    # Melt para convertir columnas en filas
        df_prop_melt = self.df.melt(
           id_vars=['id_fuente', 'region', 'año',
             'FNCE', 'GEE_final',
             'Descuento_FNCE', 'Descuento_GEE',
             'suma_EFA', 'suma_GEE',
             'Sugerencia'],  
            value_vars=value_vars,
            var_name='tipo_inversion',
            value_name='porcentaje_inversion')


    # Ajustar nombre de tipo_inversion
        df_prop_melt['tipo_inversion'] = df_prop_melt['tipo_inversion'].str.replace('_prop', '')
    
     # Filtrar solo filas con porcentaje > 0
        df_prop_melt = df_prop_melt[df_prop_melt['porcentaje_inversion'] > 0]


    # Agregar descuento según tipo de inversión
        df_prop_melt['Descuento'] = df_prop_melt.apply(
            lambda row: row['Descuento_FNCE'] if 'EFA' in row['tipo_inversion'] else row['Descuento_GEE'],
            axis=1)


        return df_prop_melt

    
