from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Authorization cases")
class TestUserGet(BaseCase):
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to get user details without auth")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Get user details test case')
    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("On this test we try to get user details while we authorized as a same user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Get user details test case')
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f'/user/{user_id_from_auth_method}',
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]

        Assertions.assert_json_has_keys(response2, expected_fields)

    # Homework - Ex16
    @allure.description("On this test we try to get user data while we authorized as another user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Get user details test case')
    def test_request_data_from_another_user(self):
        # Авторизация пользователя с id = 2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_auth = MyRequests.post('/user/login', data=data)
        auth_sid = self.get_cookie(response_auth, "auth_sid")
        token = self.get_header(response_auth, "x-csrf-token")

        # Запрос по пользователю, где id = 1 с заголовками и кукисами от авторизованного пользователя, где id = 2
        response_not_auth = MyRequests.get('/user/1',
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        not_expected_fields = ["email", "firstName", "lastName"]

        # Новая функция в библиотеке assertion.py
        Assertions.assert_json_has_not_keys(response_not_auth, not_expected_fields)
        Assertions.assert_json_has_key(response_not_auth, "username")
