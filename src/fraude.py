import duckdb
import pandas as pd
import numpy as np

def create_table(conn: duckdb.DuckDBPyConnection):
    np.random.seed(42)
    n = 10000
    data = {
        'id': range(1, n+1),
        'monto': np.random.exponential(scale=100, size=n),
        'esFraude': np.random.choice(['Y', 'N'], size=n, p=[0.05, 0.95]),
        'risk': np.random.rand(n),
    }
    df_data = pd.DataFrame(data)
    conn.register('scoring', df_data)

def get_query() -> str:
    with open("sql/query_fraude.sql", "r") as file:
        return file.read() 

def analyze_fraude(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    query = get_query()
    return conn.execute(query).fetchdf()

if __name__ == "__main__":
    conn = duckdb.connect()

    create_table(conn)
    df_data = analyze_fraude(conn)
    print(df_data.head())