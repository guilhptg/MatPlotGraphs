import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Carregar dados fictícios (substituir pelos reais)
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

# app Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div([
    
    # 🔹 Sidebar
    html.Div([
        html.H2("📊 Dashboard de Vendas", style={'color': 'black'}),
        
        html.Label("📅 Selecione um ano:", style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown_ano',
            options=[{'label': ano, 'value': ano} for ano in anos],
            value=anos[-1],
            clearable=False
        ),
        
        html.Label("📦 Filtrar por Produto:", style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown_produto',
            options=[{'label': prod, 'value': prod} for prod in produtos],
            value=produtos[0],
            clearable=False
        )
    ], style={'width': '20%', 'padding': '20px', 'background': '#222', 'black': 'white', 'position': 'fixed', 'height': '100vh'}),
    
    # 🔹 Gráficos principais
    html.Div([
        dcc.Graph(id='grafico_vendas'),
        dcc.Graph(id='grafico_produtos'),
        dcc.Graph(id='grafico_categorias'),
        dcc.Graph(id='grafico_vendas_ano')
    ], style={'margin-left': '22%', 'padding': '20px'})
])

# 🔹 4. Callbacks para atualizar os gráficos
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
    df_filtrado = df_produtos[df_produtos['Produto'] == produto_selecionado]
    fig = px.bar(df_filtrado, x='Produto', y='Quantidade', title='Quantidade de Produtos Vendidos')
    return fig

@app.callback(
    Output('grafico_categorias', 'figure'),
    [Input('dropdown_ano', 'value')]
)
def atualizar_grafico_categorias(ano_selecionado):
    fig = px.pie(df_categorias, padding=2, names='Categoria', values='Quantidade', title='Distribuição de Categorias')
    return fig

@app.callback(
    Output('grafico_vendas_ano', 'figure'),
    [Input('dropdown_ano', 'value')]
)
def atualizar_grafico_vendas_ano(ano_selecionado):
    df_ano = df_vendas_ano[df_vendas_ano['Ano'] == ano_selecionado]
    fig = px.bar(df_ano, x=['Online', 'Loja'], y=[df_ano.iloc[0]['Online'], df_ano.iloc[0]['Loja']], title='Vendas Online vs Loja')
    return fig

# 🔹 5. Rodar o app
if __name__ == '__main__':
    app.run_server(debug=True)
