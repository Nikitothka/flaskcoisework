import requests
import json
from markupsafe import Markup

class ApiHandler:
    def make_api_request(self, text):
        url = 'http://localhost:8081/api/check-plagiarism'
        headers = {
            'Content-Type': 'application/json',
            'Encryption-Key': '123'
        }
        data = {
            "text": text,
            "flag": True,
            "work_id": "фывфыв"
        }
        response = requests.post(url, headers=headers, json=data)
        return response.text

    def process_api_response(self, response):
        print(response)  # Debugging statement

        try:
            res = json.loads(response)
            keyid_size_cnt = res.get('keyid_size_cnt', {})
            text = res.get('text', '')

            if not keyid_size_cnt or not text:
                return 'Ошибка в структуре ответа API.'

            result = ''
            k = 0
            for key, val in keyid_size_cnt.items():
                a = text[k:int(key)]
                b = text[int(key):int(key) + int(val[0])]
                k += val[0]

                if a:
                    result += self.highlight_words(a, 'green')
                if b:
                    result += self.highlight_words(b, 'red')

            return Markup(result)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return 'Ошибка при обработке ответа API.'

    def highlight_words(self, text, color):
        words = text.split()
        highlighted_text = ''
        for word in words:
            highlighted_text += f'<span style="background-color: {color};">{word} </span>'
        return highlighted_text
