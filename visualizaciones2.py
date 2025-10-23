from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from kpi2 import InversionPorRegionFNCE, InversionPorRegionGEE, EvolucionAnualPorRegion, TipoInversionPredominantePorRegion

DB_NAME = "applications.db"


#DATOS
# ------------------------------

df_fnce = InversionPorRegionFNCE(DB_NAME)
df_gee = InversionPorRegionGEE(DB_NAME)
df_evolucion = EvolucionAnualPorRegion(DB_NAME)

# Unimos FNCE y GEE por región para gráfico general
df_regiones = pd.merge(df_fnce, df_gee, on="region")
df_melt_general = df_regiones.melt(
    id_vars="region",
    value_vars=["total_FNCE", "total_GEE"],
    var_name="Tipo",
    value_name="Valor"
)

# Columna en millones
df_melt_general['Valor_millones'] = df_melt_general['Valor'] / 1_000_000



#GRAFICO ------------------------------

# Gráfico general comparación FNCE vs GEE por región
fig_general = px.bar(
    df_melt_general,
    x="region",
    y="Valor",
    color="Tipo",
    barmode="group",
    title="Inversión en FNCE y GEE por región (Comparación General)",
    text='Valor_millones',
    height=450
)
fig_general.update_traces(texttemplate='%{text:.1f} M', textposition='outside')
fig_general.update_layout(
    yaxis_title="Inversión total (millones)",
    xaxis_title="Región",
    xaxis={'categoryorder':'category ascending'},
    legend_title_text="Tipo de inversión"
)

# Gráficos de línea de tiempo por región
figs_por_region = []
regiones = df_evolucion['region'].unique()
for region_name in regiones:
    df_region = df_evolucion[df_evolucion['region'] == region_name].melt(
        id_vars="año",
        value_vars=["total_FNCE", "total_GEE"],
        var_name="Tipo",
        value_name="Valor"
    )
    df_region['año'] = df_region['año'].astype(str)
    fig = px.line(
        df_region,
        x="año",
        y="Valor",
        color="Tipo",
        markers=True,
        title=f"Evolución de FNCE y GEE - {region_name}"
    )
    fig.update_layout(
        yaxis_title="Inversión total",
        xaxis_title="Año",
        legend_title_text="Tipo de inversión"
    )
    figs_por_region.append(fig)


df_top_tipo = TipoInversionPredominantePorRegion(DB_NAME)

fig_tipo_region = px.bar(
    df_top_tipo,
    x='frecuencia',
    y='region',
    color='tipo_inversion',
    orientation='h',
    text='frecuencia',
    title='Tipo de inversión predominante por región'
)
fig_tipo_region.update_traces(textposition='outside')
fig_tipo_region.update_layout(yaxis={'categoryorder':'total ascending'})


# DASH LAYOUT
# ------------------------------

app = Dash(__name__)

card_style = {
    "backgroundColor": "white",
    "padding": "20px",
    "borderRadius": "12px",
    "boxShadow": "0px 2px 6px rgba(0,0,0,0.15)",
    "marginBottom": "30px"
}

# Organizamos gráficos de línea de tiempo en grilla 2x3
grid_region_graphs = []
for i in range(0, len(figs_por_region), 2):
    row = html.Div([
        html.Div(dcc.Graph(figure=figs_por_region[i]), style={"flex": "1", **card_style}),
        html.Div(dcc.Graph(figure=figs_por_region[i+1]), style={"flex": "1", **card_style}) if i+1 < len(figs_por_region) else html.Div(style={"flex": "1"})
    ], style={"display": "flex", "gap": "20px", "marginBottom": "30px"})
    grid_region_graphs.append(row)

app.layout = html.Div(
    style={"backgroundColor": "#f4f6f9", "color": "black", "padding": "30px", "fontFamily": "Arial"},
    children=[
        html.H1("Análisis de Inversiones FNCE y GEE por Región", style={"textAlign": "center", "marginBottom": "50px"}),

        # Gráfico general FNCE vs GEE
        html.Div(dcc.Graph(figure=fig_general), style=card_style),

        # Gráfico tipo de inversión predominante por región
        html.Div(dcc.Graph(figure=fig_tipo_region), style=card_style),

        # Gráficos individuales por región (líneas de tiempo)
        *grid_region_graphs
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
