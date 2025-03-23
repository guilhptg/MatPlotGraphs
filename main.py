import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from threading import Thread

# Dados
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
vendas = [85, 90, 78, 92, 88, 96, 94, 98, 100, 102, 105, 108]
df_vendas = pd.DataFrame({'Mês': meses, 'Vendas': vendas})

produtos = ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E']
quantidades = [23, 45, 17, 30, 37]
df_produtos = pd.DataFrame({'Produto': produtos, 'Quantidade': quantidades})

categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros']
quantidades_categorias = [45, 30, 15, 10]
df_categorias = pd.DataFrame({'Categoria': categorias, 'Quantidade': quantidades_categorias})

anos = [2018, 2019, 2020, 2021]
vendas_online = [5, 10, 15, 20]
vendas_loja = [10, 8, 6, 4]
df_vendas_ano = pd.DataFrame({'Ano': anos, 'Online': vendas_online, 'Loja': vendas_loja})

# Inicialização do app Dash com Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do Dashboard
app.layout = dbc.Container([
    # Título
    dbc.Row(
        dbc.Col(html.H2("📊 Dashboard de Vendas", style={'color': 'black'}), width=12),
        className="mb-4"
    ),
    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("📅 Selecione um ano:", style={'color': 'white'}),
            dcc.Dropdown(
                id='dropdown_ano',
                options=[{'label': ano, 'value': ano} for ano in anos],
                value=anos[-1],
                clearable=False
            )
        ], width=6),
        dbc.Col([
            html.Label("📦 Filtrar por Produto:", style={'color': 'white'}),
            dcc.Dropdown(
                id='dropdown_produto',
                options=[{'label': prod, 'value': prod} for prod in produtos],
                value=produtos[0],
                clearable=False
            )
        ], width=6)
    ], className="mb-4"),
    # Gráfico de Vendas Mensais
    dbc.Row(
        dbc.Col(dcc.Graph(id='grafico_vendas'), width=12),
        className="mb-4"
    ),
    # Gráficos de Produtos e Categorias (lado a lado)
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico_produtos'), width=6),
        dbc.Col(dcc.Graph(id='grafico_categorias'), width=6)
    ], className="mb-4"),
    # Gráfico de Vendas Online vs Loja
    dbc.Row(
        dbc.Col(dcc.Graph(id='grafico_vendas_ano'), width=12)
    )
], fluid=True)

# Callbacks
@app.callback(
    Output('grafico_vendas', 'figure'),
    [Input('dropdown_ano', 'value')]
)
def atualizar_grafico_vendas(ano_selecionado):
    fig = px.line(df_vendas, x='Mês', y='Vendas', title=f'Vendas Mensais - {ano_selecionado}', markers=True)
    return fig

@app.callback(
    Output('grafico_produtos', 'figure'),
    [Input('dropdown_produto', 'value')]
)
def atualizar_grafico_produto(produto_selecionado):
    df_filtrado = df_produtos.copy()  # Evita modificação do dataframe original
    # Destaca o produto selecionado
    df_filtrado['Cor'] = df_filtrado['Produto'].apply(
        lambda x: 'yellow' if x == produto_selecionado else 'gray'
    )
    fig = px.bar(df_filtrado, x='Produto', y='Quantidade', 
                title='Quantidade de Produtos Vendidos',
                color='Cor', color_discrete_map={'yellow': 'yellow', 'gray': 'lightgray'})
    return fig

@app.callback(
    [Output('grafico_categorias', 'figure'),
    Output('grafico_vendas_ano', 'figure')],
    [Input('dropdown_ano', 'value')]
)
def atualizar_graficos(ano_selecionado):
    # Gráfico de Categorias (Pizza)
    fig_categorias = px.pie(
        df_categorias, names='Categoria', values='Quantidade', 
        title='Distribuição de Categorias', hole=0.3,
        color_discrete_sequence=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    )
    fig_categorias.update_traces(
        hoverinfo='label+percent', textinfo='value',
        textfont_size=16, marker=dict(line=dict(color='#ffffff', width=2))
    )
    
    # Gráfico de Vendas Online vs Loja (Barras)
    df_ano = df_vendas_ano[df_vendas_ano['Ano'] == ano_selecionado]
    df_fig = pd.DataFrame({
        'Tipo': ['Online', 'Loja'],
        'Vendas': [df_ano.iloc[0]['Online'], df_ano.iloc[0]['Loja']]
    })
    fig_vendas = px.bar(
        df_fig, x='Tipo', y='Vendas', 
        title=f'Vendas - Online vs Loja ({ano_selecionado})',
        color='Tipo', color_discrete_map={'Online': '#1f77b4', 'Loja': '#ff7f0e'}
    )
    return fig_categorias, fig_vendas

# Rodar o app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


def run_dash():
    app.run(debug=False, use_reloader=False, port=8050, host='0.0.0.0')

thread = Thread(target=run_dash)
thread.daemon = True
thread.start()