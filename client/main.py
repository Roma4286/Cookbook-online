from nicegui import ui
import requests

API_URL = "http://127.0.0.1:8000"

def login(username, password):
    try:
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        response.raise_for_status()
        token = response.json()["access_token"]
        ui.navigate.to('http://127.0.0.1:8080/user')
    except requests.exceptions.RequestException as e:
        ui.notify(f"Ошибка авторизации: {e.response.json().get('detail', 'Неизвестная ошибка')}", color="negative")

def register(username, email, password):
    try:
        response = requests.post(f"{API_URL}/auth/register", json={"username": username, "email": email, "password": password})
        response.raise_for_status()
        ui.notify("Регистрация прошла успешно!", color="positive")
    except requests.exceptions.RequestException as e:
        ui.notify(f"Ошибка регистрации: {e.response.json().get('detail', 'Неизвестная ошибка')}", color="negative")

def build_auth_page():
    with ui.row():
        with ui.column():
            ui.label("Авторизация")
            username_input = ui.input(label="Имя пользователя")
            password_input = ui.input(label="Пароль", password=True)
            ui.button("Войти", on_click=lambda: login(username_input.value, password_input.value))
        with ui.column():
            ui.label("Регистрация")
            reg_username_input = ui.input(label="Имя пользователя")
            reg_email_input = ui.input(label="Электронная почта")
            reg_password_input = ui.input(label="Пароль", password=True)
            ui.button("Зарегистрироваться", on_click=lambda: register(
                reg_username_input.value, reg_email_input.value, reg_password_input.value
            ))

@ui.page("/user")
def user_page():
    ui.label(f"Добро пожаловать, 1!")

ui.page("/")(build_auth_page)

ui.run(port=8080)
