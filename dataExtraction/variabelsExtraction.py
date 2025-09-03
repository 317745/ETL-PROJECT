import pandas as pd
from bs4 import BeautifulSoup

class varExtract:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r', encoding='utf-8') as xmlFile:
            self.xmlContent = BeautifulSoup(xmlFile, 'xml')

    #File extraction
    def filesExtraction1(self):
        dictFiles = {'idFile': [], 'file': [], 'description': []}
        descriptions = []

        try:
            for descr in self.xmlContent.find_all('fileDscr'):
                dictFiles['idFile'].append(descr['ID'])
                dictFiles['file'].append(descr.fileName.get_text(strip=True))
                dictFiles['description'].append(descr.fileCont.get_text(strip=True))
                descriptions.append((descr['ID'], (descr.fileCont.get_text(strip=True))))

            return {
                'ok': True,
                'data': pd.DataFrame(dictFiles),
                'msg': 'The files extraction was succesfully',
                'descr': descriptions
            }
        
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + ' 1'
            }    


    #Variabels dataset 
    def variabelsExtraction2(self):
        dictvariabels = {'idVariabel': [], 'name': [], 'varDescription': [], 'idFile': [], 'intrvl': []}

        try:
            for code in self.xmlContent.find_all('var'):
                dictvariabels['idVariabel'].append(code['ID'].strip())
                dictvariabels['name'].append(code['name'].strip())
                dictvariabels['idFile'].append(code['files'].strip())
                dictvariabels['intrvl'].append(code['intrvl'].strip())
                dictvariabels['varDescription'].append(code.labl.get_text(strip=True))

            return {
                'ok': True,
                'data': pd.DataFrame(dictvariabels),
                'msg': 'The variabels extraction was succesfully'
            }
        
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + ' 2'
            }


    #Change the file description
    def changeFileDesc3(self):
        customDesc = {
            "F19": "Gasto ambiental manufactura",
            "F20": "Gastos de gestión",
            "F21": "Gestión de residuos",
            "F22": "Manejo hídrico",
            "F23": "Gestión ambiental"
        }

        try:
            extract = self.filesExtraction1()

            if extract['ok']:
                dataExtrac = extract['data'].copy()
                dataExtrac['description'] = dataExtrac['idFile'].map(customDesc).fillna(dataExtrac['description'])
                                                                                        
                return {
                    'ok': True,
                    'data': dataExtrac,
                    'msg': 'The changes of the description was succesfully'
                }
            
            else:
                return {
                    'ok': extract['ok'],
                    'data': None,
                    'msg': extract['msg'] 
                }   
                                                                            
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + ' 3'
            }


    def dfVarMeaning4(self):
        extCodes = self.changeFileDesc3()
        extvariabels = self.variabelsExtraction2()

        try:
            if extCodes['ok'] and extvariabels['ok']:
                dfVar = pd.merge(extCodes['data'], extvariabels['data'], on='idFile')
                data = dfVar[['idFile', 'name', 'intrvl', 'description', 'varDescription']]

                return {
                    'ok': True,
                    'data': data,
                    'msg': 'Variabels extracted from the XML file'
                }  
             
            else:
                return {
                    'ok': extCodes['ok'],
                    'data': None,
                    'msg': extCodes['msg']
                } 
            
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + ' 4'
            }
        
    def file19Vars5(self):
        varMeaning = self.dfVarMeaning4()

        try:
            if varMeaning['ok']:
                df = varMeaning['data']
                data = df[df['idFile'] == 'F19']

                return {
                    'ok': True,
                    'data': (data, data[['name', 'varDescription']]),
                    'msg': 'Variabels extracted from the XML file'
                }   
            
            else:
                return {
                    'ok': varMeaning['ok'],
                    'data': None,
                    'msg': varMeaning['msg']
                } 
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + ' 5'
            }
