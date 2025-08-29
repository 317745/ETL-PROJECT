from dataExtraction.variabelsExtraction import varExtract
from dataExtraction.dfExtraction import dfGenerator

def main():
    classVar = varExtract('data/eai/variables/DANE-DIMPE-EAI-2020.xml')

    variablesF19 = classVar.file19Vars5()
    varDescription = variablesF19['data'][1].set_index('name')['varDescription'].to_dict()
    vars = list(varDescription.keys())

    classDf = dfGenerator('data/eai/chapters')
    dfs = classDf.getFiles1('.csv')
    dataFiltered = classDf.extractData2(dfs['data'], varDescription, vars)
    data = dataFiltered['data']
    df = classDf.selectCols3(data)['data']
    print(df.info())
    #df.to_csv('/home/steven/Code/codePy/etlProject/data/csvFile.csv')
    
if __name__ == '__main__':
    main()