import ipeadatapy as idpy
import pandas as pd


class GetIPEAData:
    """
    Classe que retorna a base de dados do IPEA - Preço por barril do petróleo bruto tipo Brent
    Code: EIA366_PBRENT366
    """

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.df_old_main = self.read_existing_date()
        self.db_main = self.etl_process()


    def call_ipea(self):
        """Função para chamar a api ipeadatapy"""
        self.db_oil = idpy.timeseries("EIA366_PBRENT366").reset_index()
        self.db_euro = idpy.timeseries("GM366_EREURO366").reset_index()
        self.db_dolar = idpy.timeseries("BM12_ERC12").reset_index()
        self.db_ipc = idpy.timeseries("IGP366_IPCS366").reset_index()
        self.db_nasdaq = idpy.timeseries("SGS366_NASDAQ366").reset_index()


    def transform_data(self):
        """Função para transformar dados provenientes da api ipeadatapy"""
        # Database Oil Price
        db_oil = self.db_oil.rename(columns={'RAW DATE': 'key_date', 'DATE': 'date', 'DAY': 'day', 'MONTH': 'month', 'YEAR': 'year', 'VALUE (US$)': 'oil_value_usd'}).copy()
        db_oil = db_oil.dropna(subset="oil_value_usd")
        db_oil['key_date'] = db_oil['key_date'].str[:10]
        db_oil['date'] = pd.to_datetime(db_oil['date'], format='%d.%m.%Y')
        db_oil['week_date'] = db_oil['date'].dt.day_name()
        db_oil = db_oil[['key_date', 'date', 'year', 'month', 'day', 'week_date', 'oil_value_usd']]

        # Database Euro Value
        db_euro = self.db_euro.rename(columns={'RAW DATE': 'key_date', 'DATE': 'date', 'DAY': 'day', 'MONTH': 'month', 'YEAR': 'year', 'VALUE (Euro)': 'euro_value_usd'}).copy()
        db_euro = db_euro.dropna(subset="euro_value_usd")
        db_euro['key_date'] = db_euro['key_date'].str[:10]
        db_euro['date'] = pd.to_datetime(db_euro['date'], format='%d.%m.%Y')
        db_euro['week_date'] = db_euro['date'].dt.day_name()
        db_euro = db_euro[['key_date', 'date', 'year', 'month', 'day', 'week_date', 'euro_value_usd']]

        # Database Dolar Value
        db_dolar = self.db_dolar.rename(columns={'RAW DATE': 'key_date', 'DATE': 'date', 'DAY': 'day', 'MONTH': 'month', 'YEAR': 'year', 'VALUE (R$)': 'dolar_value_brl'}).copy()
        db_dolar = db_dolar.dropna(subset="dolar_value_brl")
        db_dolar['key_date'] = db_dolar['key_date'].str[:10]
        db_dolar['date'] = pd.to_datetime(db_dolar['date'], format='%d.%m.%Y')
        db_dolar['week_date'] = db_dolar['date'].dt.day_name()
        db_dolar = db_dolar[['key_date', 'date', 'year', 'month', 'day', 'week_date', 'dolar_value_brl']]

        # Databse IPC
        db_ipc = self.db_ipc.rename(columns={'RAW DATE': 'key_date', 'DATE': 'date', 'DAY': 'day', 'MONTH': 'month', 'YEAR': 'year', 'VALUE ((% a.m.))': 'ipc_value_percent_a_m'}).copy()
        db_ipc = db_ipc.dropna(subset="ipc_value_percent_a_m")
        db_ipc['key_date'] = db_ipc['key_date'].str[:10]
        db_ipc['date'] = pd.to_datetime(db_ipc['date'], format='%d.%m.%Y')
        db_ipc['week_date'] = db_ipc['date'].dt.day_name()
        db_ipc = db_ipc[['key_date', 'date', 'year', 'month', 'day', 'week_date', 'ipc_value_percent_a_m']]

        # Database Nasdaq
        db_nasdaq = self.db_nasdaq.rename(columns={'RAW DATE': 'key_date', 'DATE': 'date', 'DAY': 'day', 'MONTH': 'month', 'YEAR': 'year', 'VALUE (-)': 'nasdaq_value'}).copy()
        db_nasdaq = db_nasdaq.dropna(subset="nasdaq_value")
        db_nasdaq['key_date'] = db_nasdaq['key_date'].str[:10]
        db_nasdaq['date'] = pd.to_datetime(db_nasdaq['date'], format='%d.%m.%Y')
        db_nasdaq['week_date'] = db_nasdaq['date'].dt.day_name()
        db_nasdaq = db_nasdaq[['key_date', 'date', 'year', 'month', 'day', 'week_date', 'nasdaq_value']]

        # MAIN DATABASE
        db_core_1 = db_oil.loc[db_oil['date'] >= '2000-01-01']
        db_merge_1 = db_euro.loc[db_euro['date'] >= '2000-01-01']
        db_stage_1 = db_core_1.merge(db_merge_1, how='left', on='key_date')
        db_stage_1 = db_stage_1.drop(columns=['date_y', 'year_y', 'month_y', 'day_y', 'week_date_y'])
        db_stage_1 = db_stage_1.rename(columns={'date_x': 'date', 'year_x': 'year', 'month_x': 'month', 'day_x': 'day', 'week_date_x': 'week_date'})

        ## db_oil + db_euro + db_dolar
        db_merge_2 = db_dolar.loc[db_dolar['date'] >= '2000-01-01']
        db_stage_2 = db_stage_1.merge(db_merge_2, how='left', on='key_date')
        db_stage_2 = db_stage_2.drop(columns=['date_y', 'year_y', 'month_y', 'day_y', 'week_date_y'])
        db_stage_2 = db_stage_2.rename(columns={'date_x': 'date', 'year_x': 'year', 'month_x': 'month', 'day_x': 'day', 'week_date_x': 'week_date'})

        ## db_oil + db_euro + db_dolar + db_ipc
        db_merge_3 = db_ipc.loc[db_ipc['date'] >= '2000-01-01']
        db_stage_3 = db_stage_2.merge(db_merge_3, how='left', on='key_date')
        db_stage_3 = db_stage_3.drop(columns=['date_y', 'year_y', 'month_y', 'day_y', 'week_date_y'])
        db_stage_3 = db_stage_3.rename(columns={'date_x': 'date', 'year_x': 'year', 'month_x': 'month', 'day_x': 'day', 'week_date_x': 'week_date'})

        ## db_oil + db_euro + db_dolar + db_ipc + db_nasdaq
        db_merge_4 = db_nasdaq.loc[db_nasdaq['date'] >= '2000-01-01']
        db_stage_4 = db_stage_3.merge(db_merge_4, how='left', on='key_date')
        db_stage_4 = db_stage_4.drop(columns=['date_y', 'year_y', 'month_y', 'day_y', 'week_date_y'])
        db_main = db_stage_4.rename(columns={'date_x': 'date', 'year_x': 'year', 'month_x': 'month', 'day_x': 'day', 'week_date_x': 'week_date'})

        return db_main


    def read_existing_date(self):
        """Função para ler base de dados existente"""
        try:
            df = pd.read_csv(self.database_path)
            return df

        except:
            return pd.DataFrame()


    def incremental_update(self, df_new: pd.DataFrame, df_old: pd.DataFrame):
        """Função para atualizar a base de dados de forma incremental"""
        # Checa se tem dados mais recentes
        df_old['date'] = pd.to_datetime(df_old['date'], format='%Y-%m-%d')
        last_date = df_old["date"].max()
        df_new_lines = df_new[df_new["date"] > last_date]

        if not df_new_lines.empty:
            df_update = pd.concat([df_old, df_new_lines], axis=0, ignore_index=True)
            return df_update

        else:
            return df_old


    def etl_process(self):
        """Processo de ETL dos dados"""
        try:
            # Chama api e transforma os dados
            self.call_ipea()
            db_main = self.transform_data()

            # Caso exista a base apenas adiciona linhas novas
            if not self.df_old_main.empty:
                db_main = self.incremental_update(db_main, self.df_old_main)

            db_main.to_csv(self.database_path, index=False)
            return db_main
        
        except Exception as e:
            # Caso exista dados na base retorna os dados existentes
            if not self.df_old_main.empty:
                return self.df_old_main
            
            else:
                input(f'\nError: {e}\n')


if __name__ == "__main__":

    df = GetIPEAData(
        database_path=".\source\teste.csv"
    )
    df.df_ipea.head()