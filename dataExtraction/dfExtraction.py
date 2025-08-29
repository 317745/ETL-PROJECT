import pandas as pd
import glob

from unidecode import unidecode

class dfGenerator:
    def __init__(self, pathFolder):
        self.pathF = pathFolder

    def getFiles1(self, extension='.csv'):
        try:
            files = glob.glob(f'{self.pathF}/*{extension}')
            return {
                    'ok': True,
                    'data': files,
                    'msg': 'Files names'
                } 
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + " 1"
            }

    def extractData2(self, file, columnsNames, columns):
        try:
            if isinstance(file, list):
                dfs = [pd.read_csv(f, sep=None, engine='python') for f in file]
                df = pd.concat(dfs, axis=0)

                df = df[columns]
                df = df.rename(columns=columnsNames)
                df.drop(columns=['Codigo unico de indentificación de las fuentes anonimizado'], inplace=True)
                df.columns = [unidecode(c.strip().lower()) for c in df.columns]
            else:
                df = [pd.read_csv(file, sep=None, engine='python')]

            return {
                'ok': True,
                'data': df,
                'msg': 'The csv transformation was succesfull'
            }
                    
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + " 2"
            }
        
    def selectCols3(self, df):
        try:
            rename_dict = {
                'inversion en maquinaria y equipo para la prevencion de la contaminacion atmosferica': 'inv_maq_prev_contaminacion',
                'inversion en construcciones y edificaciones para la prevencion de la contaminacion atmosferica': 'inv_cons_prev_contaminacion',
                'inversion total para la descontaminacion de suelos y cuerpos de agua': 'sisas',
                'mantenimiento de equipos para la prevencion de la contaminacion atmosferica': 'mant_eq_prev_contaminacion',
                'medicion, control y analisis para la prevencion de la contaminacion atmosferica': 'med_control_prev_contaminacion',
                'total costos y gastos para la prevencion de la contaminacion atmosferica': 'total_prev_contaminacion',
                'total inversion y gastos para la prevencion de la contaminacion atmosferica': 'total_inv_prev_contaminacion',
                'inversion en maquinaria y equipo para el tratamiento de gases contaminantes y material particulado.': 'inv_maq_trat_gases',
                'inversion en construcciones y edificaciones para el tratamiento de gases contaminantes y material particulado.': 'inv_cons_trat_gases',
                'total costos y gastos para el tratamiento de gases contaminantes y material particulado.': 'total_trat_gases',
                'inversion en maquinaria y equipo para el tratamiento y eliminacion de residuos peligrosos': 'inv_maq_residuos',
                'total costos y gastos para el tratamiento y eliminacion de residuos peligrosos': 'total_residuos',
                'inversion en maquinaria y equipo para la prevencion de la generacion de aguas residuales': 'inv_maq_aguas',
                'inversion total para prevencion y/o reduccion de la produccion de residuos': 'total_red_residuos',
                'total inversion y gastos para la proteccion de la biodiversidad y los ecosistemas.': 'total_prot_biodiversidad'
            }

            cols = list(rename_dict.keys())

            df = df[cols]
            df = df.rename(columns=rename_dict)
            return {
                'ok': True,
                'data': df,
                'msg': 'The selection of the columns were sucesfull'
            }
        except Exception as e:
            return {
                'ok': False,
                'data': None,
                'msg': str(e) + " 3"
            }
