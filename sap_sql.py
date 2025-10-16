import requests
import json

# import xmltodict


class Tools:
    BASEURL=""
    CLIENT=""
    USERNAME=""
    PASSWORD=""

    def __init__(self, BASEURL, CLIENT, USERNAME, PASSWORD):
        self.BASEURL=BASEURL
        self.CLIENT=CLIENT
        self.USERNAME=USERNAME
        self.PASSWORD=PASSWORD
        pass

    def get_auth_token(self, session, base_url, endpoint, username, password):
        # Аутентификация
        try:
            url = base_url + endpoint
            headers = {"X-CSRF-Token": "fetch"}
            session.auth = (username, password)
            response = session.get(url, headers=headers)
            response.raise_for_status()
            token = response.headers.get("x-csrf-token")
            if not token:
                return None
            return token
        except requests.exceptions.RequestException as e:
            return None

    def post_data_and_get_xml(self, session, base_url, endpoint, token, data_string):
        try:
            url = base_url + endpoint
            headers = {"X-CSRF-Token": token, "Content-Type": "text/plain"}
            response = session.post(
                url, headers=headers, data=data_string.encode("utf-8")
            )
#            response.raise_for_status()
#            response = response
            return response
        except requests.exceptions.RequestException as e:
            return None

    def execute_sql(self, sql) -> str:
        # Выполнение SQL-запроса в SAP
        # Путь для получения токена
        TOKEN_ENDPOINT = "/sql?sap-client="+self.CLIENT
        # Путь для POST-запроса
        POST_ENDPOINT = "/sql?sap-client="+self.CLIENT
        try:
            session = requests.Session()
            token = self.get_auth_token(
                session, self.BASEURL, TOKEN_ENDPOINT, self.USERNAME, self.PASSWORD
            )
            if token is None:
                return "Ошибка авторизации"
            response = self.post_data_and_get_xml(
                session, self.BASEURL, POST_ENDPOINT, token, sql
            )
            return response

        except Exception as e:
            print(e)
            return "Invalid equation"


if __name__ == "__main__":
    tools = Tools()
    print(tools.execute_sql("select * from t000"))
    print(tools.execute_sql("select * from t0001"))

