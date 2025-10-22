# import pandas as pd
# from plotly.subplots import make_subplots
# import sqlite3
# from kpi import (
#     InversionEvolucionAnual,
#     DescuentoPromedio,
#     RankingRegiones,
#     IndiceEficienciaEnergetica,
#     DescuentoPromedioRegion,
# )
#
# import plotly.express as px
# import plotly.graph_objects as go
# from dash import Dash, html, dcc
#
# DB_NAME = "applications.db"
#
# df_inversion = InversionEvolucionAnual(DB_NAME)
# df_descuento = DescuentoPromedio(DB_NAME)
# df_ranking = RankingRegiones(DB_NAME)
# df_indice = IndiceEficienciaEnergetica(DB_NAME)
# df_retorno = DescuentoPromedioRegion(DB_NAME)
#
# app = Dash(__name__)
#
# # KPI 1
# fig_inversion = go.Figure()
# fig_inversion.add_trace(go.Scatter(
#     x=df_inversion["año"], y=df_inversion["total_FNCE"],
#     mode="lines+markers", name="FNCE", line=dict(color="#28a745")))
# fig_inversion.add_trace(go.Scatter(
#     x=df_inversion["año"], y=df_inversion["total_GEE"],
#     mode="lines+markers", name="GEE", line=dict(color="#007bff")))
# fig_inversion.update_layout(
#     title="Evolución anual de la inversión (FNCE y GEE)",
#     xaxis_title="Año", yaxis_title="Inversión total",
#     paper_bgcolor="white", plot_bgcolor="white",
#     font=dict(family="Arial", size=14, color="black")
# )
#
# # KPI 2
# promedio_fnce = float(df_descuento["promedio_descuento_FNCE"].iloc[0])
# promedio_gee = float(df_descuento["promedio_descuento_GEE"].iloc[0])
#
# def kpi_card(title, value, color):
#     return go.Figure(go.Indicator(
#         mode="number",
#         value=value,
#         number={
#             "prefix": "$ ",
#             "valueformat": ",.0f",  # separador de miles, sin decimales
#             "font": {"size": 14, "color": color, "family": "Arial"}
#         },
#         title={"text": title, "font": {"size": 12, "color": "black", "family": "Arial"}}
#     )).update_layout(
#         paper_bgcolor="white", 
#         plot_bgcolor="white"
#     )
#
# fig_descuento_fnce = kpi_card("Descuento Promedio FNCE", promedio_fnce, "#28a745")
# fig_descuento_gee = kpi_card("Descuento Promedio GEE", promedio_gee, "#007bff")
#
# # KPI 3
# df_ranking_sorted = df_ranking.sort_values(by="total_inversion", ascending=False)
#
# fig_ranking = px.treemap(
#     df_ranking_sorted,
#     path=["region"],                   # Cada región es un cuadrito
#     values="total_inversion",          # Tamaño según inversión total
#     color="total_inversion",           # Color por inversión
#     color_continuous_scale="Blues"     # Escala de colores
# )
#
# fig_ranking.update_traces(
#     textinfo="label+value",            # Mostrar región y valor
#     hovertemplate=(
#         "<b>Región %{label}</b><br>" +
#         "Total FNCE: %{customdata[0]:,.0f}<br>" +
#         "Total GEE: %{customdata[1]:,.0f}<br>" +
#         "Inversión Total: %{value:,.0f}<extra></extra>"
#     ),
#     customdata=df_ranking_sorted[["total_FNCE", "total_GEE"]].values
# )
#
# fig_ranking.update_layout(
#     title="Mapa de calor de regiones por inversión (FNCE/GEE)",
#     paper_bgcolor="white",
#     plot_bgcolor="white",
#     font=dict(family="Arial", size=14, color="black")
# )
# # KPI 4 
#
# fig_indice = make_subplots(
#     rows=1, cols=4,  
#     specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
#     subplot_titles=[str(a) for a in sorted(df_indice["año"].unique())[:4]]  
# )
#
#
# años_unicos = sorted(df_indice["año"].unique())[:4]
#
# for i, año in enumerate(años_unicos, start=1):
#     df_año = df_indice[df_indice["año"] == año]
#     fig_indice.add_trace(
#         go.Pie(
#             labels=df_año["region"],
#             values=df_año["indice_eficiencia"],
#             name=str(año),
#             hole=0.4,
#             textinfo="none",  
#             hovertemplate="<b>%{label}</b><br>Porcentaje: %{percent}<br>Índice: %{value}<extra></extra>"  
#         ),
#         1, i
#     )
#
# fig_indice.update_layout(
#     title="Índice de Eficiencia Energética (por Año y Región)",
#     paper_bgcolor="white",
#     plot_bgcolor="white",
#     font=dict(family="Arial", size=12, color="black"),
#     showlegend=False
# )
# # KPI 5
# df_melt = df_retorno.melt(
#     id_vars="region",
#     value_vars=["total_descuento_FNCE", "total_descuento_GEE", "total_descuento"],
#     var_name="Tipo",
#     value_name="Valor"
# )
#
# fig_retorno = px.bar(
#     df_melt, x="region", y="Valor",
#     color="Tipo",
#     barmode="group",
#     title="Retorno estimado de la inversión",
#     color_discrete_map={
#         "total_descuento_FNCE": "#28a745",
#         "total_descuento_GEE": "#007bff",
#         "total_descuento": "#00ffcc"
#     }
# )
#
# fig_retorno.update_layout(
#     paper_bgcolor="white", plot_bgcolor="white",
#     font=dict(family="Arial", size=14, color="black")
# )
#
# card_style = {
#     "backgroundColor": "white",
#     "padding": "15px",
#     "borderRadius": "12px",
#     "boxShadow": "0px 2px 6px rgba(0,0,0,0.15)"
# }
#
# app.layout = html.Div(
#     style={
#         "backgroundColor": "#f4f6f9",
#         "color": "black",
#         "padding": "20px",
#         "fontFamily": "Arial"
#     },
#     children=[
#         html.H1(" Inversiones",
#                 style={"textAlign": "center", "marginBottom": "30px"}),
#
#         # Fila 1
#         html.Div([
#             html.Div(dcc.Graph(figure=fig_inversion),
#                      style={"flex": "2", **card_style}),
#             html.Div([
#                 html.Div(dcc.Graph(figure=fig_descuento_fnce),
#                          style={"flex": "1", **card_style}),
#                 html.Div(dcc.Graph(figure=fig_descuento_gee),
#                          style={"flex": "1", **card_style})
#             ], style={"flex": "1", "display": "flex", "gap": "15px"})
#         ], style={"display": "flex", "gap": "20px", "marginBottom": "30px"}),
#
#         # Fila 2
#         html.Div([
#             html.Div(dcc.Graph(figure=fig_ranking), style={"flex": "1", **card_style}),
#             html.Div(dcc.Graph(figure=fig_indice), style={"flex": "1", **card_style})
#         ], style={"display": "flex", "gap": "20px", "marginBottom": "30px"}),
#
#         # Fila 3
#         html.Div([
#             html.Div(dcc.Graph(figure=fig_retorno), style={"flex": "1", **card_style})
#         ], style={"marginBottom": "30px"})
#     ]
# )
