from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import secrets
import allure


@allure.epic("Authorization cases")
class TestUserRegister(BaseCase):
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to create user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Create user test case')
    # Позитивный код на регистрацию
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to get create user with existing auth")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Create user test case')
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"


    # Homework - Ex15-1
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to create user with incorrect email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Create user test case')
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content {response.content}. Somehow you managed to create a user with the wrong login: you missed a symbol '@' at email name."

    # Homework - Ex15-2
    exclude_params_for_email = [
        ("no_password"),
        ("no_username"),
        ("no_firstName"),
        ("no_lastName"),
        ("no_email")
    ]
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to create user without one of required fields")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Create user test case')
    # Parametrize
    @pytest.mark.parametrize('condition', exclude_params_for_email)
    def test_create_user_without_one_of_fields(self, condition):
        email = 'vinkotov@example.com'
        # New function - take a look at base_case.py
        data = self.prepare_registration_data_with_parametrize(email, condition)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {condition[3:]}", f"Unexpected response content {response.content}. Somehow you managed to create a user without the required parameters!"

    # Homework - Ex15-3
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to create user with only one symbol in email address")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Create user test case')
    def test_create_user_with_one_symbol_name(self):
        email = 'L'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'email' field is too short", f"Unexpected response content {response.content}. Somehow you managed to create a user with one symbol on a name!"

    # Homework - Ex15-4
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to create user with very long name in email address")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Create user test case')
    def test_create_user_with_very_long_name(self):
        # Using secrets lib for generating the base part of the email with chosen length
        email = f'{secrets.token_hex(251)}@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'email' field is too long", f"Unexpected response content {response.content}. Somehow you managed to create a user with more than 251 symbols on a name!"
