import sender_stand_request
import data


def get_user_body(first_name):
	current_body = data.user_body.copy()
	current_body["firstName"] = first_name
	return current_body


def positive_assert(first_name):
	user_body = get_user_body(first_name)
	user_response = sender_stand_request.post_new_user(user_body)
	print("Task 5: firstName: ", first_name)
	assert user_response.status_code == 201
	print("Task 5.1: ", user_response.status_code)
	assert user_response.json()["authToken"] != ""
	print("Task 5.2: ", user_response.json()["authToken"])
	
	users_table_response = sender_stand_request.get_users_table()
	
	str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + \
	           user_response.json()["authToken"]
	
	assert users_table_response.text.count(str_user) == 1
	print("Task 5.3: ", users_table_response.text.count(str_user))


def negative_assert_symbol(first_name):
	user_body = get_user_body(first_name)
	response = sender_stand_request.post_new_user(user_body)
	print("Task 5: firstName: ", first_name)
	assert response.status_code == 400
	print("Task 5.1: ", response.status_code)
	assert response.json()["code"] == 400
	print("Task 5.2: ", response.json()["code"])
	print("Task 5.3: ", response.json()["message"]) == "Имя пользователя введено некорректно. " \
	                                                   "Имя может содержать только русские или латинские буквы, " \
	                                                   "длина должна быть не менее 2 и не более 15 символов"


def negative_assert_no_firstname(user_body):
	response = sender_stand_request.post_new_user(user_body)
	print("Task 5: firstName: no firstName")
	assert response.status_code == 400
	print("Task 5.1: ", response.status_code)
	assert response.json()["code"] == 400
	print("Task 5.2: ", response.json()["code"])
	print("Task 5.3: ", response.json()["message"]) == "Не все необходимые параметры были переданы"


# definitions of positive tests
def test_create_user_2_letter_in_first_name_get_success_response():
	print("1")
	positive_assert("Aa")


def test_create_user_15_letter_in_first_name_get_success_response():
	print("2")
	positive_assert("Ааааааааааааааа")


def test_create_user_english_letter_in_first_name_get_success_response():
	print("3")
	positive_assert("QWErty")


def test_create_user_russian_letter_in_first_name_get_success_response():
	print("4")
	positive_assert("Мария")


# definitions of negative tests
def test_create_user_1_letter_in_first_name_get_error_response():
	print("5")
	negative_assert_symbol("A")


def test_create_user_16_letter_in_first_name_get_error_response():
	print("6")
	negative_assert_symbol("Аааааааааааааааa")


def test_create_user_has_space_in_first_name_get_error_response():
	print("7")
	negative_assert_symbol("Человек и КО")


def test_create_user_has_special_symbol_in_first_name_get_error_response():
	print("8")
	negative_assert_symbol("\"№%@\",")


def test_create_user_has_number_in_first_name_get_error_response():
	print("9")
	negative_assert_symbol("123")


def test_create_user_no_first_name_get_error_response():
	print("10")
	user_body = data.user_body.copy()
	# Удаление параметра firstName из запроса
	user_body.pop("firstName")
	negative_assert_no_firstname(user_body)


def test_create_user_empty_first_name_get_error_response():
	print("11")
	user_body = get_user_body("")
	negative_assert_no_firstname(user_body)


def test_create_user_number_type_first_name_get_error_response():
	print("12")
	user_body = get_user_body(12)
	response = sender_stand_request.post_new_user(user_body)
	print("Task 5: firstName: number type")
	assert response.status_code == 400
	print("Task 5.1: ", response.status_code)

# positive tests
# test_create_user_2_letter_in_first_name_get_success_response()
# test_create_user_15_letter_in_first_name_get_success_response()
# test_create_user_english_letter_in_first_name_get_success_response()
# test_create_user_russian_letter_in_first_name_get_success_response()
#
# # negative tests
# test_create_user_1_letter_in_first_name_get_error_response()
# test_create_user_16_letter_in_first_name_get_error_response()
# test_create_user_has_space_in_first_name_get_error_response()
# test_create_user_has_special_symbol_in_first_name_get_error_response()
# test_create_user_has_number_in_first_name_get_error_response()
# test_create_user_no_first_name_get_error_response()
# test_create_user_empty_first_name_get_error_response()
# test_create_user_number_type_first_name_get_error_response()
