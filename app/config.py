from app.mainApp import WebCalculator

web_calc = WebCalculator('127.0.0.1', '17678')  # сюда вводить HOST, PORT. По умолчанию стоит localhost, 17678.
BASE_APP_DIR = r'C:\Users\wladi\Desktop\задачи\app'  # сюда ввести дирикторию где лежить webaclculator.exe

HOST = web_calc.host
PORT = web_calc.port
URL = f'http://{HOST}:{PORT}/'
print(URL)