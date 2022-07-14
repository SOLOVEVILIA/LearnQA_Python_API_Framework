from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Authorization cases")
class TestUserEdit(BaseCase):
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to edit just created user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Edit test case')
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        # В загаловках передаем параметры которые хотим изменить и их новые значения
        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f'/user/{user_id}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")


    # Homework - Ex17-1
    TEST_CASE_LINK = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUMAJOq3hrxVMZjJM8Hu4WcOL1KRxs7vNWdH8GU9YhzqFkVE82PAIuPhEvQ9t0NJ-evc&usqp=CAU'

    @allure.description("On this test we try to edit user without authorization")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Edit test case')
    def test_edit_user_without_auth(self):
        # PREP USER FOR TEST - take only user_id from REGISTER function
        data = self.prepare_basic_login()

        # TRY TO EDIT
        # Пытаемся передать параметры которые хотим изменить и их новые значения, а так же прописать новые рандомные значения
        response2 = MyRequests.put(
            f'/user/{data["user_id"]}',
            data={"password": "new_123",
            "username": "new_learnqa",
            "firstName": "new_name",
            "lastName": "new_learnqa",
            "email": 'new_email@mail.ru'}
        )

        # Проверяем, что без авторизации не получилось сделать put-запрос (так как Auth token not supplied)'
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == "Auth token not supplied", f'Somehow you managed to change user data without login. ' \
                                                   f'Message: {response2.content}'

        # GET - проверяем, что значение username не изменилось и равно learnqa
        response3 = MyRequests.get(
            f'/user/{data["user_id"]}'
        )

        Assertions.assert_json_value_by_name(response3, "username", "learnqa",
                                             "Wait what? Somehow you managed to change user data without login.")

    # Homework - Ex17-2
    @allure.description("On this test we try to edit user with authorization from another user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Edit test case')
    def test_edit_user_with_auth_from_another_user(self):
        # REGISTER part in a separate function
        data = self.prepare_basic_login()

        # LOGIN
        login_data = {
            'email': data['email'],
            'password': data['password']
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        # Передаем параметры которые хотим изменить у другого пользователя (id указано вручную) и их новые значения
        response3 = MyRequests.put(
            f'/user/1',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        # Checking status code from the server
        Assertions.assert_code_status(response3, 200)

        # Checking content inside a request
        assert response3.content.decode("utf-8") == '', f"You managed to change the user data. " \
                                                          f"Content = {response3.content}"

        # GET info for verification
        response4 = MyRequests.get(
            f'/user/1',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(response4, "username", "Lana", "You managed to change the user data.")

    # Homework - Ex17-3
    @allure.description("On this test we try to edit user and change email on wrong name = without @ symbol")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Edit test case')
    def test_edit_user_email_without_special_symbol(self):
        # REGISTER part in a separate function
        data = self.prepare_basic_login()

        # LOGIN
        login_data = {
            'email': data['email'],
            'password': data['password']
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        # Создаем новый email без спец.символа = @
        new_email = "ChangedMailWithoutSpecialSymbol.com"

        # Передаем параметры которые хотим изменить - email
        response3 = MyRequests.put(
            f'/user/{data["user_id"]}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        # Проверяем, что изменить email не получилось
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == 'Invalid email format', \
            f'You managed to change email. Content = {response3.content}'

        # GET
        # Сравниваем фактическое значение email
        response4 = MyRequests.get(
            f'/user/{data["user_id"]}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(response4, "email", data['email'], "You managed to change email.")

    # Homework - Ex17-4
    @allure.description("On this test we try to edit user and give firstName the wrong length = only one symbol in name")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(TEST_CASE_LINK, 'Edit test case')
    def test_edit_user_firstName_one_symbol(self):
        # REGISTER part in a separate function
        data = self.prepare_basic_login()

        # LOGIN
        login_data = {
            'email': data['email'],
            'password': data['password']
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        # Заводим имя с длиной = один символ
        new_name = "A"

        # Передаем параметры которые хотим изменить
        response3 = MyRequests.put(
            f'/user/{data["user_id"]}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        # Проверяем, что ничего не смогли изменить
        Assertions.assert_code_status(response3, 400)
        assert response3.json()["error"] == 'Too short value for field firstName', \
            f'You managed to change the name using only one symbol. Content: {response3.content}'

        # GET
        # Сравниваем фактическое значение firstName
        response4 = MyRequests.get(
            f'/user/{data["user_id"]}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(response4, "firstName", data['firstName'], "Wrong name of the user after edit")
