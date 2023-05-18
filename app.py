import time

from flask import Flask, render_template, request
from flask_cors import CORS
from file_handler import FileHandler
from api_handler import ApiHandler

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']

    try:
        work_id =  request.values['new-work-name']
    except KeyError:
        work_id =  request.values['work-select']
    print(work_id)
    if uploaded_file.filename != '':
        start_time = time.time()

        file_handler = FileHandler(uploaded_file)
        if file_handler.save_file():
            text = file_handler.get_text()
            api_handler = ApiHandler()

            response, status_code = api_handler.make_api_request(text,work_id=work_id)
            result = api_handler.process_api_response(response,status_code)

            execution_time = time.time() - start_time

            time_html = f'<div class="execution-time">Execution Time: {execution_time:.2f} seconds</div>'
            result_html = render_template('result.html', result=result, time=time_html)

            return result_html
        else:
            return 'Ошибка при сохранении файла.'

    return 'Ошибка при загрузке файла.'

if __name__ == '__main__':
    app.run(debug=False, port=8080)
