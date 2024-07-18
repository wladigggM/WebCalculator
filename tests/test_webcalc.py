import os
import pytest
import requests

from app.config import BASE_APP_DIR, URL, web_calc

os.chdir(BASE_APP_DIR)


@pytest.mark.parametrize(
    "api_action, variables",
    [
        ('/api/state', None),
        ('/api/addition', {"x": 2, "y": 2}),
        ('/api/multiplication', {"x": 2, "y": 2}),
        ('/api/division', {"x": 2, "y": 2}),
        ('/api/remainder', {"x": 2, "y": 2}),
    ]
)
def test_valid_action(api_action, variables):
    web_calc.start()
    # Проверяем работоспособность state
    if api_action == '/api/state':

        response = requests.get(URL + api_action)
        assert response.status_code == 200

        data = response.json()
        assert data['statusCode'] == 0
        assert data['state'] == 'OК'
        # Проверяем работоспособность и правильность выполнения остальных методов
    else:

        response = requests.post(URL + api_action, json=variables)
        assert response.status_code == 200

        data = response.json()
        if api_action == '/api/addition':
            assert data['result'] == variables['x'] + variables['y']
        elif api_action == '/api/multiplication':
            assert data['result'] == variables['x'] * variables['y']
        elif api_action == '/api/division':
            assert data['result'] == variables['x'] / variables['y']
        elif api_action == '/api/remainder':
            assert data['result'] == variables['x'] % variables['y']
    web_calc.stop()


@pytest.mark.parametrize(
    "api_action, variables, statusCode",
    [
        ("/api/division", {"x": 42, "y": 0}, 1),  # Деление на ноль. Код ошибки почему то 8 хотя в ПРИЛОЖЕНИИ код 1 !!!
        ("/api/addition", {"x": 42}, 2),  # Отсутствующие ключи
        ("/api/addition", {"x": "invalid", "y": 24}, 3),  # Неверный формат входных данных
        ("/api/addition", {"x": 2147483649, "y": 24}, 4),  # Переполнение числа
        ("/api/addition", {"invalid_json"}, 5),  # Неправильный формат тела запроса
    ]
)
# Проверка негативных случаев
def test_negative_cases(api_action, variables, statusCode):
    web_calc.start()
    # Проверка на "Неправильный формат тела запроса" требует другого типа данных для запроса
    if statusCode == 5:

        response = requests.post(URL + api_action, data=variables)

        data = response.json()
        assert data["statusCode"] == 5
        # print('\n============================= RESULT =============================\n', 'statusCode:',
        #       data["statusCode"],
        #       data["statusMessage"], '\n==================================================================\n')
    else:
        response = requests.post(URL + api_action, json=variables)
        data = response.json()
        assert "statusMessage" in data
        assert data["statusCode"] == statusCode
        # print('\n============================= RESULT =============================\n', 'statusCode',
        #       data["statusCode"],
        #       data["statusMessage"], '\n==================================================================\n')
    web_calc.stop()


# Проверяем функционал управления приложением
def test_app():
    new_data = {}
    action = {'start': web_calc.start,
              'restart': web_calc.restart,
              'show_logs': web_calc.show_log,
              'show_help': web_calc.show_help
              }
    for key, command in action.items():
        # Записываю отчет логов/хелпа/рестарта, чтобы убедится что все работает
        if key == 'show_logs':
            new_data['logs'] = command()
        elif key == 'restart':
            new_data['restart'] = command()
        elif key == 'show_help':
            new_data['help'] = command()
            # Для старта проверки команды start делаю запрос к /api/state и смотрю ответ
        else:
            command()
            response = requests.get(URL + '/api/state')  # Изменение URL(HOST/PORT) в config.py
            assert response.status_code == 200
            data = response.json()
            assert data["statusCode"] == 0
            assert data["state"] == 'OК'

    assert 'help' in new_data
    assert 'logs' in new_data
    assert 'restart' in new_data
    # У объекта web_calc имеется атрибут is_running который хранит в себе значение типа bool
    web_calc.stop()
    assert not web_calc.is_running  # Проверяем остановилась ли работ приложения


"""
    Проверка на смену host/port,
    а так же старт без указания параметров не имеет смысла
    т.к. в созданном мною классе эти атрибуты по умолчанию идут: localhost 17678
"""
