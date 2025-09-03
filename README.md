# ETL Project: Análisis de Inversiones Ambientales en la Industria Manufacturera Colombiana

## 📌 Descripción del Proyecto

Este proyecto ETL (Extract, Transform, Load) procesa datos de la Encuesta Ambiental Industrial (EAI) del DANE para analizar las inversiones y gastos en protección ambiental realizados por la industria manufacturera colombiana entre 2019-2022. El sistema genera insights sobre descuentos tributarios, eficiencia energética y retorno de inversión ambiental.

## 🏗️ Estructura del Proyecto

etlProject/
├── data/
│ ├── csvFile.csv
│ └── eai/
│ ├── chapters/
│ │ ├── ANONIMIZADO_CAP2_19.csv
│ │ ├── ANONIMIZADO_CAP2_20.csv
│ │ ├── ANONIMIZADO_CAP2_21.csv
│ │ ├── ANONIMIZADO_CAP2_22.csv
│ │ └── ETL_Workshop-1.pdf
│ └── variables/
│ └── DANE-DIMPE-EAI-2020.xml
├── dataExtraction/
│ ├── dfExtraction.py
│ └── variabelsExtraction.py
├── dataTransform/
│ ├── dataTransformation.py
│ └── resultTransformation.py
├── Load/
│ └── dataLoad.py
├── main.py
├── kpi.py
├── visualizaciones.py
├── test_kpi.py
├── applications.db
├── requirements.txt
└── README.md


## 🔧 Tecnologías Utilizadas

- **Python 3.12+**
- **Pandas** - Manipulación de datos
- **SQLite** - Base de datos dimensional
- **Dash** - Visualizaciones interactivas
- **BeautifulSoup (bs4)** - Parseo de XML
- **ETL Framework** - Proceso completo de extracción, transformación y carga

## 📊 Esquema de Base de Datos

### Tablas de Dimensiones
```sql
CREATE TABLE DimEmpresa (
    id_fuente REAL PRIMARY KEY
)

CREATE TABLE DimRegion (
    region TEXT PRIMARY KEY
)

CREATE TABLE DimAño (
    año INTEGER PRIMARY KEY
)

CREATE TABLE DimTipoInversion (
    tipo_inversion TEXT PRIMARY KEY
)
```

### Tabla de Hechos 

```sql

CREATE TABLE FactInversiones (
    id_fuente INTEGER,
    region TEXT,
    año INTEGER,
    FNCE,
    GEE_final,
    Descuento_FNCE,
    Descuento_GEE,
    suma_EFA,
    suma_GEE,
    tipo_inversion TEXT,
    porcentaje_inversion,
    Sugerencia
)

```

# 🚀 Instalación y Uso

## 1. Configurar entorno virtual
python -m venv .venvEtl
source .venvEtl/bin/activate  # Linux/Mac
.venvEtl\Scripts\activate  # Windows

## 2. Instalar dependencias
pip install -r requirements.txt

## 3. Ejecutar pipeline ETL completo y visualizaciones
python main.py

## 5. Ejecutar tests de validación
python test_kpi.py

# Estructura esperada de archivos y directorios

etlProject/
├── data/                    # Directorio principal de datos
│   └── eai/                 # Datos de la Encuesta Ambiental Industrial
│       ├── chapters/        # Capítulos de la encuesta por año
│       │   ├── ANONIMIZADO_CAP2_19.csv
│       │   ├── ANONIMIZADO_CAP2_20.csv
│       │   ├── ANONIMIZADO_CAP2_21.csv
│       │   └── ANONIMIZADO_CAP2_22.csv
│       └── variables/       # Metadata y definiciones de variables
│           └── DANE-DIMPE-EAI-2020.xml
│
├── dataExtraction/          # Módulo de extracción de datos
│   ├── dfExtraction.py
│   └── variabelsExtraction.py
│
├── dataTransform/           # Módulo de transformación de datos
│   ├── dataTransformation.py
│   └── resultTransformation.py
│
├── Load/                    # Módulo de carga de datos
│   └── dataLoad.py
│
├── main.py                  # Script principal de ejecución
├── kpi.py                   # Cálculo de indicadores clave
├── visualizaciones.py       # Generación de visualizaciones
├── test_kpi.py              # Tests de validación
├── requirements.txt         # Dependencias de Python
└── README.md                # Documentación del proyecto

Nota: Los directorios __pycache__ y archivos .db son generados automáticamente
durante la ejecución y no necesitan ser incluidos manualmente
## 📋 Requisitos del sistema:
- Python 3.12 o superior
- 8GB RAM recomendados
- 2GB espacio libre en disco
- Conexión a internet para instalación de paquetes

## 📋 Proceso ETL

### 🔍 Extracción (Extract)
- **Fuentes de datos**: 4 datasets de la Encuesta Ambiental Industrial (EAI) del DANE (2019-2022)
- **Volumen inicial**: 2940 columnas por dataset
- **Selección estratégica**: 148 variables relevantes del Capítulo 2
- **Metadatos**: Parseo de archivos XML para estructura de variables
- **Años procesados**: 2019, 2020, 2021, 2022

### 🔄 Transformación (Transform)
- **Validación de datos**: Verificación de cálculos empresariales reportados
- **Detección de inconsistencias**: Identificación de reportes erróneos o incompletos
- **Normalización temporal**: Unificación de formatos de fecha y periodos
- **Cálculo de métricas**:
  - Eficiencia energética (GEE_final)
  - Descuentos tributarios (Descuento_FNCE, Descuento_GEE)
  - Porcentajes de inversión ambiental
- **Estimaciones**: Proyección de descuentos tributarios aplicables

### 📤 Carga (Load)
- **Modelo de base de datos**: Esquema dimensional en SQLite
- **Tablas creadas**:
  - 4 tablas de dimensiones (DimEmpresa, DimRegion, DimAño, DimTipoInversion)
  - 1 tabla de hechos (FactInversiones)
- **Optimización**: Índices y relaciones para consultas eficientes
- **Output final**: Datos estructurados para análisis y reporting

### 📊 Flujo del Pipeline
1. **Extracción inicial** → Datos brutos de archivos CSV
2. **Limpieza básica** → Eliminación de duplicados y valores nulos
3. **Transformación específica** → Cálculos de métricas ambientales
4. **Validación final** → Control de calidad de datos
5. **Carga en BD** → Almacenamiento en modelo dimensional
6. **Generación de reportes** → Informes automatizados por empresa

### ⚙️ Herramientas de Transformación
- **Pandas**: Manipulación avanzada de datos
- **Funciones personalizadas**: Cálculos específicos del dominio ambiental
- **Validaciones cruzadas**: Consistencia entre años y variables
- **Algoritmos de estimación**: Proyección de beneficios tributarios

### 🎯 Salidas del Proceso
- **Base de datos SQLite** con schema optimizado
- **Dataset consolidado** listo para análisis
- **Métricas calculadas** para cada empresa
- **Sugerencias automatizadas** de inversión ambiental
- **Data quality report** con indicadores de calidad