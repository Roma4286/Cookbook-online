import requests
from nicegui import ui

ui.run()

def nicegui_interface():
    ui.label("Введите ваше имя и возраст:")
    name_input = ui.input(label="Имя")
    age_input = ui.input(label="Возраст")

    # Функция отправки данных
    async def submit_data():
        name = name_input.value
        age = int(age_input.value)
        response = requests.post('http://127.0.0.1:8000/submit/', json={"name": name, "age": age})
        if response.status_code == 200:
            print(1)
            ui.notify(response.json().get("message"))
        else:
            ui.notify("Ошибка при отправке данных.")

    ui.button("Отправить", on_click=submit_data)

nicegui_interface()