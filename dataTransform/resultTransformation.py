from dataTransform.dataTransformation import transformation
import pandas as pd
import numpy as np
import os

#Este .py solo sirve para revisar resultados no esta en main.py

# Cargar datos
df = pd.read_csv(r'C:\Users\Admin\Documents\GitHub\ETL-PROJECT\data\csvFile.csv', encoding='utf-8')

# Crear carpeta de salida si no existe
output_dir = r'C:\Users\Admin\Documents\GitHub\ETL-PROJECT\output_csv'
os.makedirs(output_dir, exist_ok=True)

# Crear instancia de la clase
tf = transformation(df)


tf.FNCE_comprobation()
tf.GEE_comprobation()

columnas_finales_descuento = [
    'id_fuente',
    'suma_EFA', 'suma_GEE', 'Descuento_FNCE', 'Descuento_GEE',
    'FNCE', 'GEE', 'GEE_final'
]

df_descuento = tf.df[columnas_finales_descuento]


df_descuento.to_csv(os.path.join(output_dir, "descuento_EFA_GEE.csv"), index=False)

#2. Análisis de inversión por tipo de activo


tf.FNCE_comprobation()
tf.GEE_comprobation()

tf.FNCE_proportion()
tf.GEE_proportion()

efa_prop_cols = [c for c in tf.df.columns if 'EFA_prop' in c]
gee_prop_cols = [c for c in tf.df.columns if 'GEE_prop' in c]


columnas_finales_proporcion = ['id_fuente', 'FNCE', 'GEE_final'] + efa_prop_cols + gee_prop_cols

df_proporcion = tf.df[columnas_finales_proporcion]
df_proporcion.to_csv(os.path.join(output_dir, "proporcion_por_activo.csv"), index=False)


#3. Inversion en region


tf.FNCE_comprobation()
tf.GEE_comprobation()
tf.FNCE_proportion()
tf.GEE_proportion()

tf.df['Sugerencia'] = np.where(
    tf.df['FNCE'] > tf.df['GEE_final'],
    "Considerar invertir en GEE",
    "Considerar invertir en EFA"
)


columnas_finales_region = [
    'id_fuente',
    'region',
    'FNCE',            
    'Descuento_FNCE', 
    'GEE_final',      
    'Descuento_GEE',
    'Sugerencia'
]


df_region = tf.df[columnas_finales_region]


df_region.to_csv(os.path.join(output_dir, "analisis_region_por_empresa.csv"), index=False)

