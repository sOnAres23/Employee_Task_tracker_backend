import requests

from config.settings import TELEGRAM_URL, API_TOKEN_TELEGRAM


def send_message(task):
    """Функция отправки сообщения пользователю о задаче в телеграм"""
    message = f'Вам назначена задача: "{task.title}"😎 дэдлайн её выполнения: {task.deadline.strftime('%d.%m.%Y')}⏰'
    chat_id = task.employee.tg_chat_id
    params = {
        'text': message,
        'chat_id': chat_id
    }
    # Отправляем запрос на API телеграма сформированным URL
    requests.get(f"{TELEGRAM_URL}{API_TOKEN_TELEGRAM}/sendMessage", params=params)
