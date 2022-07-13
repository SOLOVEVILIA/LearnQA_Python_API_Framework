import json.decoder
from requests import Response
from datetime import datetime

from lib.my_requests import MyRequests
from lib.assertions import Assertions


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find headers with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        # Убеждаемся, что ответ пришел в формате json, а не в каком-то другом
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    # Функция, котороая помогает подготавливать регистрационные данные
    # Тут email - это входной параметр с дефлотным значением
    # Это значит, что при вызове данной функции, email можно передавать, а можно не передавать

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f'{base_part}{random_part}@{domain}'
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    # Homework - Ex15-2
    def prepare_registration_data_with_parametrize(self, email=None, condition=None):
        # NO PASSWORD
        if condition == "no_password":
            return {
                'password': None,
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }
        # NO USERNAME
        if condition == "no_username":
            return {
                'password': '123',
                'username': None,
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email
            }
        # NO FIRSTNAME
        if condition == "no_firstName":
            return {
                'password': '123',
                'username': 'learnqa',
                'firstName': None,
                'lastName': 'learnqa',
                'email': email
            }
        # NO LASTNAME
        if condition == "no_lastName":
            return {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': None,
                'email': email
            }
        # NO EMAIL
        if condition == "no_email":
            return {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': None
            }

    # Homework - Ex17-0 // Only register part
    def prepare_basic_login(self):
        # REGISTER PART
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        return {
                'password': password,
                'username': 'learnqa',
                'firstName': first_name,
                'lastName': 'learnqa',
                'email': email,
                'user_id': user_id
            }
