import subprocess
import time
import requests
import asyncio

# Настройки сервера Rasa
RASA_SERVER_COMMAND = "rasa run -m models --enable-api --cors \"*\" --debug"


def process_rasa_request(user_message):
    # Отправляем запрос на сервер Rasa
    response = requests.post("http://localhost:5005/webhooks/rest/webhook", json={"message": user_message}).json()

    if response:
        # Получаем ответы от сервера Rasa
        bot_response = "\n".join([r['text'] for r in response])
        return bot_response


async def run_rasa_server():
    # Запуск сервера Rasa
    rasa_process = subprocess.Popen(RASA_SERVER_COMMAND, shell=True)

    # Ожидание запуска сервера Rasa
    time.sleep(10)

    # Ожидание завершения сервера Rasa
    while True:
        if rasa_process.poll() is not None:
            break
        await asyncio.sleep(1)

    # Завершение процесса сервера Rasa
    rasa_process.terminate()
    rasa_process.wait()
