from dataExtraction.variabelsExtraction import varExtract
from dataExtraction.dfExtraction import dfGenerator
from dataTransform.dataTransformation import transformation

import sqlite3
from Load.dataLoad import load_dw

def main():
    classVar = varExtract('data/eai/variables/DANE-DIMPE-EAI-2020.xml')

    variablesF19 = classVar.file19Vars5()
    varDescription = variablesF19['data'][1].set_index('name')['varDescription'].to_dict()
    vars = list(varDescription.keys())
    vars.append('year')

    classDf = dfGenerator('data/eai/chapters')
    dfs = classDf.getFiles1('.csv')
    dataFiltered = classDf.extractData2(dfs['data'], varDescription, vars)
    data = dataFiltered['data']
    df = classDf.selectCols3(data)['data']
    df.to_csv(r'data/csvFile.csv', index=False, encoding='utf-8')


    # Transformación ----------
    transform = transformation(df)
    transform.FNCE_comprobation()
    transform.GEE_comprobation()
    transform.FNCE_proportion()
    transform.GEE_proportion()
    df_fact = transform.create_fact_table()
    
    df_fact = transform.create_fact_table()

    # Load---------------------
    conn = sqlite3.connect('applications.db')
    load_dw(conn, df_fact)
    conn.close()

    # -------------------------------
    # Visualizaciones (Dash) - ejecutar después de ETL
    # -------------------------------
    from visualizaciones2 import app
    app.run(debug=True)


if __name__ == '__main__':
    main()
