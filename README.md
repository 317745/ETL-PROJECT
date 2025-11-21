# ETL Project: Analysis of Environmental Investments in the Colombian Manufacturing Industry

## 📌 Project Description
This ETL (Extract, Transform, Load) project processes data from the Environmental Industrial Survey (EAI) of DANE to analyze investments and expenses in environmental protection made by the Colombian manufacturing industry between 2019-2022. The system generates insights on tax discounts, energy efficiency, and environmental investment returns.

## 🏗️ Project Structure

![Project Structure](structure/structureProject.png)


## 🔧 Technologies Used
- **Python 3.12+**
- **Pandas** - Data manipulation
- **SQLite** - Dimensional database
- **Dash** - Interactive visualizations
- **BeautifulSoup (bs4)** - XML parsing
- **ETL Framework** - Complete extraction, transformation, and loading process

## 📊 Database Schema
### Dimension Tables
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

### Fact Table

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

# 🚀 Installation and Usage


## 1. Set up virtual environment
python -m venv .venvEtl
source .venvEtl/bin/activate  # Linux/Mac
.venvEtl\Scripts\activate  # Windows

## 2. Install dependencies
pip install -r requirements.txt

## 3. Run complete ETL pipeline and visualizations
python main.py

## 4. Run validation tests
python test_kpi.py

# Expected File and Directory Structure

![Expected File and Directory Structure](structure/image.png)

Note: __pycache__ directories and .db files are automatically generated during execution and do not need to be included manually.

## 📋 Requisitos del sistema:
- Python 3.12 o superior
- 8GB RAM recomendados
- 2GB espacio libre en disco
- Conexión a internet para instalación de paquetes

## 📋 System Requirements:
- Python 3.12 or higher
- 8GB RAM recommended
- 2GB free disk space
- Internet connection for package installation

## 📋 ETL Process — Second Delivery

The second delivery extends the initial ETL pipeline by incorporating **data enrichment through API integration**, **process automation with Apache Airflow**, and **dashboards built with Dash (Plotly)**.  
These improvements enhanced scalability, traceability, and the analytical capacity of the environmental investment dataset.

---

### 🔍 1. Extraction (Extract)

In this phase, data are collected and consolidated from multiple sources:

- **DANE CSV files (EAI)**: Corresponding to the years **2019–2022**, each dataset containing approximately **2,940 columns**.  
- **Colombian Public API (api-colombia.com)**: Accessed via Swagger from a Jupyter Notebook using the `requests` and `pandas` libraries.  
  This source provided official information on **regions** and **departments**, strengthening the geographical dimension of the analysis.  
- **XML files**: Containing metadata and variable structure, used to identify and extract the **148 relevant variables** from *Chapter 2* of the EAI.

This combination of sources enabled the creation of a **complete, updated, and validated dataset** for subsequent pipeline stages.

---

### 🔄 2. Transformation (Transform)

During this stage, data cleansing, validation, and enrichment were performed within the `dataTransformation.py` module.  
The main operations include:

- **Data validation**: Verification of reported values and business calculations.  
- **Error handling**: Identification and correction of incomplete or inconsistent records.  
- **Temporal normalization**: Standardization of reference dates and reporting periods.  
- **Metric calculations**:
  - Energy Efficiency and Clean Power Generation (**GEE_final**, **FNCE**)  
  - Tax Credits (**Descuento_FNCE**, **Descuento_GEE**)  
  - Environmental Investment Percentages  
- **Estimations**: Projection of potential tax benefits and returns associated with environmental investments.  
- **Data enrichment**: Incorporation of regional and departmental information obtained from the API.

This phase guarantees **data quality, consistency, and analytical reliability**.

---

### 📤 3. Loading (Load)

The transformed data are stored in a **SQLite database** structured under a **dimensional model**, implemented in the `dataLoad.py` module.

**Database structure:**
- **Dimension Tables**:
  - `DimEnterprise`  
  - `DimRegion`  
  - `DimYear`  
  - `DimTypeInvestment`
- **Fact Table**:
  - `FactInversiones`: Consolidates investments by company, region, year, and type of investment.  

Additionally, the **API-derived regional and departmental data** were integrated into the corresponding dimension tables to enhance geospatial analysis.

---

### ⚙️ 4. Pipeline Flow and Automation

The entire ETL flow is automated and orchestrated by **Apache Airflow**, using the `etl_run_scripts.py` script as the main controller.  
This automation ensures **consistency, traceability, and scheduled execution** of the process.

**Execution order:**
1. **Extraction** → Data retrieval from CSV, XML, and API sources.  
2. **Transformation** → Data cleaning, validation, and environmental metric computation.  
3. **Loading** → Insertion of transformed data into the SQLite dimensional schema.  
4. **Visualization** → Automatic update of KPIs and charts in the **Dash (Plotly)** dashboard, including:
   - Energy efficiency indicators  
   - Regional investment heatmaps  
   - Annual investment evolution

---

---

### 📊 Pipeline Flow Overview
1. **Extraction** → Automatic data retrieval from EAI and Colombia API.  
2. **Cleaning & Validation** → Removal of duplicates and missing data handling.  
3. **Transformation** → Energy and tax-related metric calculations.  
4. **Enrichment** → Integration of regional and geographic information.  
5. **Load** → Storage into a dimensional SQLite database.  
6. **Automation** → Scheduled and monitored through Apache Airflow.  
7. **Analysis & Visualization** → Interactive dashboards and KPIs built with Dash.


### ⚙️ Transformation Tools
- **Pandas**: Advanced data manipulation
- **Custom functions**: Domain-specific environmental calculations
- **Cross-validations**: Consistency between years and variables
- **Estimation algorithms**: Projection of tax benefits

### 🎯 Process Outputs
- **SQLite database** with optimized schema
- **Consolidated dataset** ready for analysis
- **Calculated metrics** for each company
- **Automated suggestions** for environmental investment
- **Data quality report** with quality indicators

## 🚀 Successful Project Execution

### ✅ Data Warehouse Status
- **DW loaded successfully**: All tables have been updated
- **Connection established**: SQLite database operational
- **Data consolidated**: 2019-2022 information processed

### 🌐 Visualization Server
- **Dash running at**: http://127.0.0.1:8050/
- **Debug mode**: Enabled for development
- **Flask application**: 'visualizaciones' running

### 📊 Graphics Access
You can access interactive visualizations by:
1. Open your web browser
2. Navigate to: http://127.0.0.1:8050/
3. Explore available dashboards

### 📈 Available Charts
- **Heat map** of investments by region
- **Annual evolution** of FNCE vs GEE investments
- **Energy efficiency** by year and region
- **Estimated return** on environmental investment
- **Comparative metrics** between companies

### ⚡ Next Steps
1. **Navigate** to the provided address
2. **Interact** with filters and charts
3. **Export** customized reports
4. **Analyze** automated suggestions

### 🛠️ Troubleshooting
If you cannot access:
- Verify that port 8050 is available
- Confirm firewall allows local connections
- Restart server if necessary

The system is ready to use! 🎉
