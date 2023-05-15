
import re
import requests
import json
import logging
from markupsafe import Markup

# Создаем логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class ApiHandler:
    def make_api_request(self, text, work_id, flag=True):
        url = 'http://localhost:8081/api/check-plagiarism'
        headers = {
            'Content-Type': 'application/json',
            'Encryption-Key': '123'
        }
        data = {
            "text": text,
            "flag": flag,
            "work_id": work_id
        }

        # Добавляем логгирование перед отправкой запроса
        logger.debug(f"Making API request with data: {data}")

        response = requests.post(url, headers=headers, json=data)

        # Добавляем логгирование после получения ответа
        logger.debug(f"Received API response: {response.text}, Status Code: {response.status_code}")

        return response.text, response.status_code

    def process_api_response(self, response, status_code):
        # Добавляем логгирование перед обработкой ответа
        logger.debug(f"Processing API response: {response}, Status Code: {status_code}")

        try:
            res = json.loads(response)
            keyid_size_cnt = res.get('keyid_size_cnt', {})
            text = res.get('text', '')
            percent = res.get('result', '')

            if status_code == 206:
                return 'File is empty'
            elif not text:
                return 'Ошибка в структуре ответа API.'
            elif not(keyid_size_cnt):
                result = Markup(f'<h1>Уникальность текста {percent:.2f} %</h1> <p>{text}</p>')
                return result

            result = ''
            k = 0
            text = re.sub(r'\\u([\dA-Fa-f]{4})', lambda m: chr(int(m.group(1), 16)), text)
            for key, val in keyid_size_cnt.items():
                a = text[k:int(key)]
                b = text[int(key):int(key) + int(val[0])]
                k = int(key)+ int(val[0])

                if a:
                    result += self.highlight_words(a, '1')
                if b:
                    if int(val[1]) > 2:
                        result += self.highlight_words(b, 'red')
                    else:
                        result += self.highlight_words(b, 'orange')
                if k > len(text):
                    result += self.highlight_words(text[k:], '1')
                    break
            result += self.highlight_words(text[k:], '1')

            return Markup(f'<h1>Уникальность текста {percent:.2f} %</h1> <p>{result}</p>')
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
            return 'Ошибка при обработке ответа API.'

    def highlight_words(self, text, color):
        # words = text.split()
        highlighted_text = ''
        # for word in words:
        highlighted_text += f'<span style="background-color: {color};">{str(text)} </span>'
        return highlighted_text
