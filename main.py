import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Carregar dados podem ser atribuidos as viráveis, e colunas editadas para ultilização dos gráficos
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do Dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            # 🔹 Sidebar
            dbc.Col([
                # 🔹 Gráficos principais
                dcc.Graph(id='grafico_vendas'),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='grafico_produtos'), width=6),
                        html.Div([
                            html.Label("📦 Filtrar por Produto:", style={'color': 'white'}),
                            dcc.Dropdown(
                                id='dropdown_produto',
                                options=[{'label': prod, 'value': prod} for prod in produtos],
                                value=produtos[0],
                                clearable=False
                            )
                        ]),
                    dbc.Col(dcc.Graph(id='grafico_categorias'), width=6)
                ]),
                    html.Div([
                        html.H2("📊 Dashboard de Vendas", style={'color': 'black'}),
                        
                        html.Label("📅 Selecione um ano:", style={'color': 'white'}),
                        dcc.Dropdown(
                            id='dropdown_ano',
                            options=[{'label': ano, 'value': ano} for ano in anos],
                            value=anos[-1],
                            clearable=False
                        ),
                    ]),
                dcc.Graph(id='grafico_vendas_ano')
            ])
        ])
    ])
], fluid=True)


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
    df_filtrado = df_produtos.copy()  # Copiamos para evitar modificar o original
    
    # Criamos uma coluna de cores: se for o produto selecionado, recebe 'eyellow', senão 'gray'
    df_filtrado['Cor'] = df_filtrado['Produto'].apply(
        lambda x: 'yellow' if x == produto_selecionado else 'gray'
    )
    fig = px.bar(df_produtos, x=df_produtos['Produto'], y=df_produtos['Quantidade'], color=df_filtrado['Cor'], title='Quantidade de Produtos Vendidos', color_discrete_map={'red': 'red', 'gray': 'lightgray'})
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
        color_discrete_sequence=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # Cores personalizadas
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
        df_fig, x='Tipo', y='Vendas', title=f'Vendas - Online vs Loja ({ano_selecionado})',
        color='Tipo', color_discrete_map={'Online': '#1f77b4', 'Loja': '#ff7f0e'}  # Azul e Laranja
    )

    return fig_categorias, fig_vendas


# 🔹 5. Rodar o app
if __name__ == '__main__':
    app.run(debug=True)
