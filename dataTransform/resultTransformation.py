from dataTransform.dataTransformation import transformation
import pandas as pd
import numpy as np
import os
from pathlib import Path

# === Configuración de rutas portables ===
BASE_DIR = Path(__file__).resolve().parents[1]   # /opt/airflow/project
DATA_DIR = BASE_DIR / "data"                     # carpeta data
OUTPUT_DIR = BASE_DIR / "output_csv"             # carpeta de salida

# Crear carpeta de salida si no existe
OUTPUT_DIR.mkdir(exist_ok=True)

# === 1. Cargar datos ===
input_csv = DATA_DIR / "csvFile.csv"
df = pd.read_csv(input_csv, encoding="utf-8")

# === 2. Crear instancia de la clase principal ===
tf = transformation(df)

# === 3. Descuento EFA y GEE ===
tf.FNCE_comprobation()
tf.GEE_comprobation()

columnas_finales_descuento = [
    "id_fuente",
    "suma_EFA", "suma_GEE", "Descuento_FNCE", "Descuento_GEE",
    "FNCE", "GEE", "GEE_final"
]

df_descuento = tf.df[columnas_finales_descuento]
df_descuento.to_csv(OUTPUT_DIR / "descuento_EFA_GEE.csv", index=False, encoding="utf-8")

# === 4. Análisis de inversión por tipo de activo ===
tf.FNCE_comprobation()
tf.GEE_comprobation()
tf.FNCE_proportion()
tf.GEE_proportion()

efa_prop_cols = [c for c in tf.df.columns if "EFA_prop" in c]
gee_prop_cols = [c for c in tf.df.columns if "GEE_prop" in c]

columnas_finales_proporcion = ["id_fuente", "FNCE", "GEE_final"] + efa_prop_cols + gee_prop_cols

df_proporcion = tf.df[columnas_finales_proporcion]
df_proporcion.to_csv(OUTPUT_DIR / "proporcion_por_activo.csv", index=False, encoding="utf-8")

# === 5. Análisis por región ===
tf.FNCE_comprobation()
tf.GEE_comprobation()
tf.FNCE_proportion()
tf.GEE_proportion()

tf.df["Sugerencia"] = np.where(
    tf.df["FNCE"] > tf.df["GEE_final"],
    "Considerar invertir en GEE",
    "Considerar invertir en EFA"
)

columnas_finales_region = [
    "id_fuente",
    "region",
    "FNCE",
    "Descuento_FNCE",
    "GEE_final",
    "Descuento_GEE",
    "Sugerencia"
]

df_region = tf.df[columnas_finales_region]
df_region.to_csv(OUTPUT_DIR / "analisis_region_por_empresa.csv", index=False, encoding="utf-8")

print("Transformación completada correctamente ✅")
print(f"Archivos guardados en: {OUTPUT_DIR}")
