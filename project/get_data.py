import ipeadatapy as idpy
import pandas as pd


class GetIPEAData:
    """
    Classe que retorna a base de dados do IPEA - Preço por barril do petróleo bruto tipo Brent
    Code: EIA366_PBRENT366
    """

    def __init__(self, ipea_table: str, database_path: str) -> None:
        self.ipea_table = ipea_table
        self.database_path = database_path
        self.df_old = self.read_existing_date()
        self.df_brent_oil = self.etl_process()


    def call_ipea(self):
        """Função para chamar a api ipeadatapy"""
        df = idpy.timeseries(self.ipea_table).reset_index()
        return df


    def transform_data(self, df: pd.DataFrame):
        """Função para transformar dados provenientes da api ipeadatapy"""
        df = df[["DATE", "VALUE (US$)"]].copy()
        df = df.rename(columns={"DATE": "date", "VALUE (US$)": "value"})
        df = df.dropna(subset="value")
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df


    def read_existing_date(self):
        """Função para ler base de dados existente"""
        try:
            df = pd.read_csv(self.database_path)
            return df

        except FileNotFoundError:
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
            df_ipea_brent_oil = self.call_ipea()
            df_ipea_brent_oil = self.transform_data(df_ipea_brent_oil)

            # Caso exista a base apenas adiciona linhas novas
            if not self.df_old.empty:
                df_ipea_brent_oil = self.incremental_update(df_ipea_brent_oil, self.df_old)

            df_ipea_brent_oil.to_csv(self.database_path, index=False)
            return df_ipea_brent_oil
        
        except Exception as e:
            # Caso exista dados na base retorna os dados existentes
            if not self.df_old.empty:
                return self.df_old
            
            else:
                input(f'\nError: {e}\n')


if __name__ == "__main__":

    df = GetIPEAData(
        ipea_table="EIA366_PBRENT366",
        database_path=".\source\ipea_brent_oil.csv"
    )
    df.df_ipea.head()