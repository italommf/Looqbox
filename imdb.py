import pandas           as pd
import streamlit        as st
from common.utils       import Utils
import plotly.express   as px

utils = Utils()

imdb_movies = utils.select(
    query = "SELECT * FROM IMDB_movies",
    return_df = True
)

st.title("Insights - IMDB")

# ==================================================================================================#
# Mapa de calor - Nota x Duração

df = imdb_movies.copy()
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df = df.dropna(subset=['Rating', 'Runtime'])

bins = list(range(60, 180, 10))
labels = [f"{b}-{b+9} min" for b in bins[:-1]]
df['Runtime_bin'] = pd.cut(df['Runtime'], bins=bins, labels=labels, right=False)
df['Rating_bin'] = df['Rating'].round(1)

contagem = df.groupby(['Runtime_bin', 'Rating_bin']).size().reset_index(name='count')
pivot = contagem.pivot(index='Runtime_bin', columns='Rating_bin', values='count').fillna(0)

fig = px.imshow(
    pivot,
    labels = dict(x = "Nota IMDb", y = "Faixa de Duração", color = "Número de Filmes"),
    x = pivot.columns,
    y = pivot.index,
    color_continuous_scale = 'thermal',
    aspect = 'auto',
    title = 'Mapa de Calor - Distribuição de notas no IMDB de acordo com a duração do filme'
)
st.plotly_chart(fig, use_container_width = True)

# ==================================================================================================#
# Gráfico - Diretor x Receita x Nota média

df_grouped = df.groupby('Director').agg(
    {
        'RevenueMillions': 'mean',
        'Rating': 'mean'
    }
).reset_index()

df_grouped['RevenueMillions'] = pd.to_numeric(df_grouped['RevenueMillions'], errors='coerce')
df_grouped['Rating'] = pd.to_numeric(df_grouped['Rating'], errors='coerce')
df_grouped = df_grouped.dropna(subset=['RevenueMillions', 'Rating'])
df_grouped = df_grouped.sort_values('RevenueMillions', ascending=False).head(30)

fig = px.scatter(
    df_grouped,
    x = 'Director',
    y = 'Rating',
    size = 'RevenueMillions',
    color = 'RevenueMillions',
    labels = {
        'Director': 'Diretor',
        'Rating': 'Nota Média',
        'RevenueMillions': 'Receita Média (Milhões)'
    },
    title = 'Diretor x Receita Média x Nota Média',
    size_max = 40,
    hover_data = {'RevenueMillions': ':.2f', 'Rating': ':.2f'}
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# ==================================================================================================#
# Gráfico - Nota média x Ano de lançamento

df = imdb_movies.copy()

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df = df.dropna(subset=['Year', 'Rating'])
df_ano = df.groupby('Year')['Rating'].mean().reset_index()

fig = px.line(
    df_ano,
    x='Year',
    y='Rating',
    title='Nota Média dos Filmes por Ano',
    labels={'Year': 'Ano de Lançamento', 'Rating': 'Nota Média'},
    markers=True
)
st.plotly_chart(fig, use_container_width=True)