import subprocess
import chardet


class WebCalculator:

    # Инициализируем объект
    def __init__(self, host: str = 'localhost', port: str = '17678', is_running: bool = False):
        self.host = host
        self.port = port
        self.is_running = is_running

    # Статик метод для выполнения команд
    @staticmethod
    def _execute_command(command):
        try:
            output = subprocess.check_output(command)
            encoding = chardet.detect(output)['encoding']
            return output.decode(encoding)
        except subprocess.CalledProcessError as e:
            encoding = chardet.detect(e.output)['encoding']
            print(f'Команда завершилась с ошибкой: {e.output.decode(encoding)}')
        except FileNotFoundError:
            print("Файл webcalculator.exe не найден.")
        except Exception as e:
            print(f"Произошла неожиданная ошибка: {str(e)}")

    # Команда старт
    def start(self):
        if self._execute_command(['webcalculator.exe', 'start', self.host, self.port]):
            self.is_running = True

    # Команда стоп
    def stop(self):
        if self._execute_command(['webcalculator.exe', 'stop']):
            self.is_running = False

    # Команда рестарт
    @classmethod
    def restart(cls):
        restart_text = cls._execute_command(['webcalculator.exe', 'restart'])
        return restart_text

    # Команда показа логов
    @classmethod
    def show_log(cls):
        log_text = cls._execute_command(['webcalculator.exe', 'show_log'])
        return log_text

    # Команда помощи
    @classmethod
    def show_help(cls):
        help_text = cls._execute_command(['webcalculator.exe', '--help'])
        return help_text


def main():
    web_calc = WebCalculator()
    web_calc.start()
    web_calc.stop()


if __name__ == '__main__':
    main()
