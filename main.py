from dataExtraction.variabelsExtraction import varExtract
from dataExtraction.dfExtraction import dfGenerator
from dataTransform.dataTransformation import transformation
<<<<<<< HEAD
from dataQuality import dq_raw_dane
from Load.dataLoad import load_dw

import sqlite3


def main():

    # -------------------- Extract --------------------
    classVar = varExtract('data/eai/variables/DANE-DIMPE-EAI-2020.xml')
    variablesF19 = classVar.file19Vars5()

=======

import sqlite3
from Load.dataLoad import load_dw

def main():
    classVar = varExtract('data/eai/variables/DANE-DIMPE-EAI-2020.xml')

    variablesF19 = classVar.file19Vars5()
>>>>>>> a3444f351782da21601c24841af946ca5ee96b6c
    varDescription = variablesF19['data'][1].set_index('name')['varDescription'].to_dict()
    vars = list(varDescription.keys())
    vars.append('year')

    classDf = dfGenerator('data/eai/chapters')
    dfs = classDf.getFiles1('.csv')
<<<<<<< HEAD

    dataFiltered = classDf.extractData2(dfs['data'], varDescription, vars)
    data = dataFiltered['data']

    df = classDf.selectCols3(data)['data']
    df.to_csv('data/csvFile.csv', index=False, encoding='utf-8')

    # Quality Check -----------------------------------
    dq_raw_dane(df)

    # -------------------- Transform --------------------
    transform = transformation(df)

=======
    dataFiltered = classDf.extractData2(dfs['data'], varDescription, vars)
    data = dataFiltered['data']
    df = classDf.selectCols3(data)['data']
    df.to_csv(r'data/csvFile.csv', index=False, encoding='utf-8')


    # Transformación ----------
    transform = transformation(df)
>>>>>>> a3444f351782da21601c24841af946ca5ee96b6c
    transform.FNCE_comprobation()
    transform.GEE_comprobation()
    transform.FNCE_proportion()
    transform.GEE_proportion()
<<<<<<< HEAD

    df_fact = transform.create_fact_table()

    # -------------------- Load -------------------------
=======
    df_fact = transform.create_fact_table()
    
    df_fact = transform.create_fact_table()

    # Load---------------------
>>>>>>> a3444f351782da21601c24841af946ca5ee96b6c
    conn = sqlite3.connect('applications.db')
    load_dw(conn, df_fact)
    conn.close()

<<<<<<< HEAD
    # -------------------- Visualizaciones (Dash) -------
=======
    # -------------------------------
    # Visualizaciones (Dash) - ejecutar después de ETL
    # -------------------------------
>>>>>>> a3444f351782da21601c24841af946ca5ee96b6c
    from visualizaciones2 import app
    app.run(debug=True)


<<<<<<< HEAD
if __name__ == "__main__":
=======
if __name__ == '__main__':
>>>>>>> a3444f351782da21601c24841af946ca5ee96b6c
    main()
