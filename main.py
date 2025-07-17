import pandas               as pd
from common.utils           import Utils
from common.conexao_mysql   import Looqbox_BD

cursor =    Looqbox_BD().cursor
utils =     Utils()

# ==================================================================================================#
# SQL TEST

# 1 - Quais os 10 produtos mais caros da empresa?
itens_mais_caros = utils.select(
    query = "SELECT PRODUCT_NAME, PRODUCT_VAL " \
            "FROM data_product "                \
            "ORDER BY PRODUCT_VAL DESC "        \
            "LIMIT 10",
    return_df = True
)
print(itens_mais_caros)

# 2 - Quais seções tem os departamentos "BEBIDAS" e "PADARIA"?
secoes = utils.select(
    query = "SELECT DISTINCT SECTION_NAME "     \
            "FROM data_product "                \
            "WHERE DEP_NAME = 'BEBIDAS' "       \
            "OR DEP_NAME = 'PADARIA'",
    return_df = True
)
print(secoes)

# 3 - Qual o total de vendas de cada área de negócio no primeiro trimestre de 2019?
vendas_q1 = utils.select(
    query = "SELECT "  
            "info_lojas.BUSINESS_NAME AS area_negocio, "                                        \
            "  SUM(produto_vendas.SALES_VALUE) AS total_vendas "                                \
            "FROM data_product produto "                                                        \
            "JOIN data_product_sales produto_vendas "                                           \
            "  ON produto.PRODUCT_COD = produto_vendas.PRODUCT_CODE "                           \
            "JOIN data_store_cad info_lojas "                                                   \
            "  ON produto_vendas.STORE_CODE = info_lojas.STORE_CODE "                           \
            "WHERE produto_vendas.DATE >= '2019-01-01' AND produto_vendas.DATE < '2019-04-01' " \
            "GROUP BY info_lojas.BUSINESS_NAME; ",
    return_df = True
)
print(vendas_q1)

# ==================================================================================================#
# CASES

# 1 - Função dinâmica para select com base em parâmetros opcionais de coódigo do produto, código da loja, lista com data inicial e data final
select_dinamico = utils.retrieve_data(
    product_code =  18,
    store_code =    1,
    date =          ['2019-01-01', '2019-01-02']
)
print(select_dinamico)

# 2 - Tabela: Loja | Categoria | TM
select_data_store_cad = utils.select(
    query =  "SELECT "                  \
             "      STORE_CODE, "       \
             "      STORE_NAME, "       \
             "      START_DATE, "       \
             "      END_DATE, "         \
             "      BUSINESS_NAME, "    \
             "      BUSINESS_CODE "     \
             "FROM data_store_cad ",
             return_df = True
)
            
select_data_store_sales = utils.select(
    query = "SELECT "                   \
            "        STORE_CODE, "      \
            "        DATE, "            \
            "        SALES_VALUE, "     \
            "        SALES_QTY "        \
            "FROM data_store_sales "    \
            "WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31' ",
            return_df = True
)

df_merge = pd.merge(
    select_data_store_cad, 
    select_data_store_sales, 
    on = 'STORE_CODE', 
).drop(
    columns = [
        'START_DATE', 
        'END_DATE', 
        'DATE', 
        'STORE_CODE', 
        'BUSINESS_CODE'
    ]
)   
df_agrupado = df_merge.groupby(['STORE_NAME', 'BUSINESS_NAME'], as_index = False).sum()

df_tm = pd.DataFrame(
    {
        'Loja':         df_agrupado['STORE_NAME'],
        'Categoria':    df_agrupado['BUSINESS_NAME'],
        'TM':           round(df_agrupado['SALES_VALUE'] / df_agrupado['SALES_QTY'], 2)
    }
)
print(df_tm)

# 3 - IMDB_movies
imdb_movies = utils.select(
    query = "SELECT * FROM IMDB_movies",
    return_df = True
)
# TODO Executar no Console: streamlit run imdb.py
