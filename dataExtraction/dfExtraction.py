import pandas as pd
import glob
import re

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
                    dfs = []
                    for f in file:
                        df_temp = pd.read_csv(f, sep=None, engine='python')
                        match = re.search(r'_(\d{2})\.csv$', f)

                        #It only works for 2000s
                        if match:
                            yearShort = 2000 + int(match.group(1))
                            df_temp['year'] = yearShort

                        dfs.append(df_temp)

                    df_temp = pd.concat(dfs, axis=0)

                    df_temp.columns = [unidecode(c.strip().lower()) for c in df_temp.columns]

                    df_temp = df_temp[[c.lower() for c in columns]]

                    df = df_temp.rename(columns={k.lower(): v.lower().rstrip('.') for k, v in columnsNames.items()})

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
                # IDS (DIM)
                'codigo unico de indentificación de las fuentes anonimizado': 'id_fuente',
                'codigo de los grupos de divisiones industriales': 'cod_div_ind',
                'codigo región': 'region',
                'year': 'año',

                # Auto-generación de energía de fuentes alternativas
                'inversión en tierras y terrenos para  la auto-generación de energía de fuentes alternativas': 'inv tierras y terrenos EFA',
                'inversión en maquinaria y equipo para la auto-generación de energía de fuentes alternativas': 'inv maquinaria y equipo EFA',
                'inversión en construcciones y edificaciones para auto-generación de energía de fuentes alternativas': 'inv construcciones y edificaciones EFA',
                'inversión total para la auto-generación de energía de fuentes alternativas': 'inversión total EFA',
                'materiales y suministros para la auto-generación de energía de fuentes alternativas': 'materiales y suministros EFA',
                'pequeñas herramientas para la auto-generación de energía de fuentes alternativas': 'pequeñas herramientas EFA',
                'mantenimiento de equipos para la auto-generación de energía de fuentes alternativas': 'mantenimiento de equipos EFA',
                'medición, control y análisis para la auto-generación de energía de fuentes alternativas': 'medición, control y análisis EFA',
                'total costos y gastos para  la auto-generación de energía de fuentes alternativas': 'total costos y gastos EFA',
                'total inversión y gastos para la auto-generación de energía de fuentes alternativas': 'total inversión y gastos EFA',

                # Reducción del consumo de recursos energéticos no renovables (GEE)
                'inversión en maquinaria y equipo para la reducción del consumo de recursos energéticos no renovables': 'inv maquinaria y equipo (GEE)',
                'inversión en construcciones y edificaciones para reducción del consumo de recursos energéticos no renovables': 'inv construcciones y edificaciones (GEE)',
                'inversión total para la reducción del consumo de recursos energéticos no renovables': 'inversión total (GEE)',
                'materiales y suministros para la reducción del consumo de recursos energéticos no renovables': 'materiales y suministros (GEE)',
                'pequeñas herramientas para la reducción del consumo de recursos energéticos no renovables': 'pequeñas herramientas (GEE)',
                'mantenimiento de equipos para la reducción del consumo de recursos energéticos no renovables': 'mantenimiento de equipos (GEE)',
                'medición, control y análisis para la reducción del consumo de recursos energéticos no renovables': 'medición, control y análisis (GEE)',
                'total costos y gastos para  la reducción del consumo de recursos energéticos no renovables': 'total costos y gastos (GEE)',
                'total inversión y gastos para la reducción del consumo de recursos energéticos no renovables': 'total inversión y gastos (GEE)'
            }


            cols = list(rename_dict.keys())
            df = df[cols]
            df = df.rename(columns=rename_dict)
            df["id_fuente"] = df.iloc[:, 0].combine_first(df.iloc[:, 1])
            df = df.loc[:, ~df.columns.duplicated()]
            
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
       



