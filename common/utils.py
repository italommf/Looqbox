import pandas               as pd
from datetime               import datetime
from common.conexao_mysql   import Looqbox_BD

class Utils(Looqbox_BD):

    def select(self, query, return_df = None):

        self.cursor.execute(query)
        dados_select_cursor = self.cursor.fetchall()

        if return_df:
            colunas_df = [coluna_db[0] for coluna_db in self.cursor.description]
            df_select = pd.DataFrame(dados_select_cursor, columns = colunas_df)
            return df_select
        
        return dados_select_cursor

    def retrieve_data(self, product_code = None, store_code = None, date = None):

        def _iso_date(date):

            if not isinstance(date, list):
                return False

            for item in date:
                try:
                    datetime.strptime(item, "%Y-%m-%d")
                except (ValueError, TypeError):
                    return False

            return True
        
        filtros = []
        query = 'SELECT * FROM data_product_sales'
        
        if product_code:
            filtros.append(f"PRODUCT_CODE = {int(product_code)}")

        if store_code:
            filtros.append(f"STORE_CODE = {int(store_code)}")

        if date:

            if len(date) == 2 and _iso_date(date):
                filtros.append(f"DATE >= '{date[0]}' AND DATE <= '{date[1]}'")
            else:
                print('[Erro] Quantidade de datas erradas no parâmetro "date". A Query foi executada sem o parâmetro de datas!')
                return

        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        return self.select(query, return_df = True)