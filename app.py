import time

from flask import Flask, render_template, request
from file_handler import FileHandler
from api_handler import ApiHandler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        start_time = time.time()  # Start time for measuring execution time

        # Add loading animation HTML
        loading_html = '<div class="loading-animation"></div>'
        result_html = render_template('result.html', result=loading_html)

        file_handler = FileHandler(uploaded_file)
        if file_handler.save_file():
            text = file_handler.get_text()
            api_handler = ApiHandler()

            response = api_handler.make_api_request(text)
            result = api_handler.process_api_response(response)

            execution_time = time.time() - start_time  # Calculate execution time

            # Add execution time HTML
            time_html = f'<div class="execution-time">Execution Time: {execution_time:.2f} seconds</div>'
            result_html = render_template('result.html', result=result, time=time_html)

            return result_html
        else:
            return 'Ошибка при сохранении файла.'

    return 'Ошибка при загрузке файла.'

if __name__ == '__main__':
    app.run(debug=True, port=8080)
