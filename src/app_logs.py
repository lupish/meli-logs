import pandas as pd

def get_app_logs() -> pd.DataFrame:
    df_logs = pd.read_csv("data/logs.csv")
    return df_logs

def clean_app_logs(df_logs: pd.DataFrame) -> pd.DataFrame:
    print(len(df_logs))

    df_logs.drop_duplicates(inplace=True) # remover duplicados exactos
    df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'], errors='coerce') # poner nulas las fechas invalidas
    df_logs.dropna(inplace=True) # remover nulos

    pattern_user_id = r'^user_\d+$'
    df_logs = df_logs[df_logs['user_id'].str.match(pattern_user_id, na=False)] # remover usuarios invalidos


    print(len(df_logs))
    return df_logs

def detect_anomalies(actions: pd.Series):
    status_need_login_before = ["logout", "purchase", "update_profile"]
    anomalies = set()
    
    status_login = False
    for a in actions:
        if a == "login":
            if status_login:
                anomalies.add("repeted_login")
            status_login = True
        elif a in status_need_login_before:
            if not status_login:
                anomalies.add(f"{a}_without_login")
            if a == "logout":
                status_login = False
    return anomalies

def get_anomalies(df_logs: pd.DataFrame) -> pd.DataFrame:
    df_logs = df_logs.sort_values(by=['user_id', 'timestamp'])
    df_anomalies_by_user = df_logs.groupby('user_id')['action'].apply(detect_anomalies)

    anomalies_users = df_anomalies_by_user[df_anomalies_by_user.apply(len) > 0]
    return anomalies_users

def get_top_users(df_logs: pd.DataFrame) -> pd.DataFrame:
    date = pd.Timestamp.today() - pd.DateOffset(months=1)
    df_data = df_logs[df_logs['timestamp'] >= date] # mes corrido

    unique_actions = df_data.groupby('user_id')['action'].nunique()
    top_5 = unique_actions.sort_values(ascending=False).head(5)
    return top_5.reset_index(name='unique_action_count')

def save_anomalies(df_anomalies: pd.DataFrame):
    df_anomalies = anomalies_users.reset_index()
    df_anomalies.columns = ['user_id', 'anomalies']
    df_anomalies['anomalies'] = df_anomalies['anomalies'].apply(lambda x: ', '.join(x))
    df_anomalies.to_csv('data/anomalies_users.csv', index=False)

if __name__ == "__main__":
    print("***************************** BEGIN *****************************")
    df_logs = get_app_logs()
    df_logs_cleaned = clean_app_logs(df_logs)

    anomalies_users = get_anomalies(df_logs_cleaned)
    pd.set_option('display.max_colwidth', None)
    save_anomalies(anomalies_users)
    print(anomalies_users)

    df_logs_valid_users = df_logs_cleaned[~df_logs_cleaned['user_id'].isin(anomalies_users)]

    df_top_users = get_top_users(df_logs_valid_users)
    print(df_top_users)

    print("****************************** END ******************************")