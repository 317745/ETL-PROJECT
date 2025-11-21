import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import json
import plotly.express as px
import plotly.graph_objects as go
import os

app = dash.Dash(__name__)

STATE_FILE = "stream_state.json"

# ---------------------------
# CACHE PARA EVITAR GRAFICOS EN BLANCO
# ---------------------------
cache_data = {}   # datos válidos más recientes


# ---------------------------
# LECTURA SEGURA DEL JSON
# ---------------------------
def obtener_datos_desde_archivo():
    global cache_data

    if not os.path.exists(STATE_FILE):
        return cache_data

    try:
        with open(STATE_FILE) as f:
            contenido = f.read().strip()

            if contenido == "":
                return cache_data   # mantener datos previos

            nuevo = json.loads(contenido)

            # actualizar cache
            cache_data = nuevo
            return nuevo

    except json.JSONDecodeError:
        return cache_data  # si está corrupto, no actualizar


# ---------------------------
# LAYOUT DEL DASHBOARD
# ---------------------------
app.layout = html.Div([
    dcc.Interval(id='interval', interval=1300, n_intervals=0),
    html.Div([
        dcc.Graph(id='investment-region-graph', style={"width": "50%", "margin": "0px"}),
        dcc.Graph(id='avg-investment-year-max-graph',   style={"width": "45%"})
    ], style={"display": "flex"}),

    html.Div([
        dcc.Graph(id='investment-type-graph', style={"width": "50%", "padding": "0px"}),
        dcc.Graph(id='investment-total-type-graph', style={"width": "45%"})
    ], style={"display": "flex"}),
    
    dcc.Graph(id='total-discount-fnce-graph'),
    dcc.Graph(id='avg-investment-year-graph')
])


# ---------------------------
# CALLBACK PRINCIPAL
# ---------------------------
@app.callback(
    [
        Output('investment-region-graph', 'figure'),
        Output('investment-type-graph', 'figure'),
        Output('investment-total-type-graph', 'figure'),
        Output('total-discount-fnce-graph', 'figure'),
        Output('avg-investment-year-graph', 'figure'),
        Output('avg-investment-year-max-graph', 'figure')
    ],
    [Input('interval', 'n_intervals')]
)
def actualizar(n):
    s = obtener_datos_desde_archivo()

    # --- GRAFICO 1 ---
    fig_investment_region = px.bar(
        s.get('investment-region', []),
        x='region', y='total_investment',
        title='Inversión por región'
    )

    fig_investment_region.update_layout(height=400, width=700)

    # --- GRAFICO 2 ---

    fig_investment_total_type = px.bar(
        s.get('investment-total-type', []),
        x='tipo_inversion', y='total_investment',
        title='Inversión total por tipo'
    )

    fig_investment_total_type.update_layout(height=400, width=700)
    
    # --- GRAFICO 3 ---

    fig_investment_type = px.pie(
        s.get('investment-type', []),
        names='tipo_inversion', values='total',
        title='Inversión por tipo', hole=0.4
    )

    fig_investment_type.update_layout(height=400)

    # --- GRAFICO 4 ---
    fig_total_discount_fnce = px.bar(
        s.get('total-discount-fnce', []),
        x='department', y='total_discount_fnce',
        title='Descuento FNCE total por departamento'
    )

    # --- GRAFICO 5 ---
    fig_avg_investment_year = px.bar(
        s.get('avg-investment-year', []),
        x='year', y='avg_investment',
        title='Inversión promedio por año'
    )

    fig_avg_investment_year.update_layout(height=500)

    # --- GRAFICO 6 (Tarjeta limpia) ---
    datos_max = s.get('avg-investment-year-max', [])

    if isinstance(datos_max, list) and len(datos_max) > 0:
        year = datos_max[-1].get("year", "N/A")
        valor = datos_max[-1].get("avg_investment", "N/A")

        fig_card = go.Figure()

        fig_card.add_annotation(
            x=2.5, y=3.5, showarrow=False,
            text="<span style='font-size:26px; font-weight:bold;'>Año con mayor inversión promedio</span>"
        )

        fig_card.add_annotation(
            x=2.5, y=2, showarrow=False,
            text=f"<span style='font-size:48px; font-weight:bold; color:#0A69B8;'>{year}</span>"
        )

        fig_card.add_annotation(
            x=2.5, y=0.2, showarrow=False,
            text=f"<span style='font-size:23px;'>${valor:,}</span>"
        )

        fig_card.update_xaxes(visible=False)
        fig_card.update_yaxes(visible=False)

        fig_card.update_layout(
            height=300,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            showlegend=False
        )
    else:
        fig_card = go.Figure()

    return (
        fig_investment_region,
        fig_card,
        fig_investment_total_type,
        fig_avg_investment_year,
        fig_investment_type,
        fig_total_discount_fnce
    )


app.run(debug=True)
