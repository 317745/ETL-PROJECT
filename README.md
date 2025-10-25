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

In the second delivery, the ETL pipeline was expanded and improved based on the first version.  
The process now includes **data enrichment through API integration**, **automation using Apache Airflow**, and **KPI visualization with Dash**.  
These additions enhance scalability, reproducibility, and analytical depth for environmental investment analysis.

---

### 🔍 Extraction (Extract)
- **Data sources**: 4 datasets from the *Environmental Industrial Survey (EAI)* of DANE (2019–2022).  
- **Initial volume**: 2,940 columns per dataset.  
- **Strategic selection**: 148 relevant variables from Chapter 2.  
- **Metadata processing**: XML file parsing to extract variable structure.  
- **External integration**: Added data from the **Colombia API** to enrich datasets with geographic details (regions and departments).  
- **Processed years**: 2019, 2020, 2021, and 2022.  
- **Automation**: Extraction tasks are now part of an **Apache Airflow DAG**, ensuring repeatable and schedulable data pipelines.

---

### 🔄 Transformation (Transform)
- **Data validation**: Verification of business and energy-related calculations.  
- **Error detection**: Identification of incomplete or inconsistent records.  
- **Temporal normalization**: Standardization of date and period formats.  
- **Metric calculations**:
  - Energy efficiency (*GEE_final*).  
  - Tax deductions for investments in *FNCE* and *GEE*.  
  - Percentage of environmental investment relative to total assets.  
- **Data enrichment**: Added region names from the external API.  
- **Estimation models**: Projection of potential tax benefits aligned with government energy policies.  
- **Integration for analysis**: Generation of key performance indicators (*KPIs*) for visualization and reporting.

---

### 📤 Loading (Load)
- **Database model**: Dimensional schema implemented in SQLite.  
- **Created tables**:
  - 4 dimension tables: *DimEmpresa*, *DimRegion*, *DimAño*, *DimTipoInversion*.  
  - 1 fact table: *FactInversiones*.  
- **Optimization**:
  - Indexed key fields (region, year, investment type).  
  - Established relationships for analytical queries.  
- **Final output**: Structured and optimized dataset for further analysis and visualization.

---

### ⚙️ Automation with Airflow
- Implementation of a **fully automated pipeline** using **Apache Airflow**.  
- Each ETL stage (Extract, Transform, Load) is defined as an individual *task* in the DAG.  
- Enables **monitoring**, **error recovery**, and **data lineage tracking**.  
- Guarantees **reproducibility** and **consistency** of the entire ETL process.

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
