from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    # Homework - Ex18-1
    def test_del_user_with_id_2(self):
        # LOGIN
        email = 'vinkotov@example.com',
        password = '1234'

        login_data = {
            'email': email,
            'password': password
        }

        response = MyRequests.post('/user/login', data=login_data)

        #print(response.status_code, response.content)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        # DELETE
        response_del = MyRequests.delete(
            f'/user/2/',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверяем, что система вернула 400 и не дала удалить пользователя
        Assertions.assert_code_status(response_del, 400)
        assert response_del.content.decode("utf-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f'You delete test user! Content = {response_del.content}'

        # Check the user after delete attempt
        response_check = MyRequests.get(
            f'/user/2',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        # if status_code == 200 - user exists
        Assertions.assert_code_status(response_check, 200)

    # Homework - Ex18-2
    def test_del_user(self):
        # REGISTER - можно использовать функцию из Ex17, которую я сделал для ДЗ
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        #first_name = register_data['firstName']
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

        # DELETE
        response_del = MyRequests.delete(
            f'/user/{user_id}/',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # If status_code == 200 - user was deleted
        Assertions.assert_code_status(response_del, 200)

        # GET - check system with user_id which was deleted
        response3 = MyRequests.get(
            f'/user/{user_id}',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        # If status_code = 404 - user doesn't exists
        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("utf-8") == 'User not found', \
            f"You didn't delete user! Content = {response3.content}"

    # Homework - Ex18-3
    def test_try_to_del_user_but_auth_from_another_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        #user_id = self.get_json_value(response1, "id")
        #print(user_id)

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # try to DELETE user with id = 2
        response_del = MyRequests.delete(
            f'/user/2',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # If status_code == 200 - the request was successfully run
        # but it doesn't mean that the user was deleted - let's check this
        Assertions.assert_code_status(response_del, 200)

        # GET - check system with user_id which was deleted / Check user after "success" delete
        response3 = MyRequests.get(
            f'/user/2',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 200)
        assert response3.json()["username"] == 'Vitaliy', \
            f"You delete user! Content = {response3.content}"
