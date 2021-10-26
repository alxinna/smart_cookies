from flask import Flask, render_template, request

from models.databasemanager import DatabaseManager

app = Flask(__name__)
test = DatabaseManager().get_test('15 Minutes Test')


@app.route('/')
def index():
    return render_template('index.html')


def check_results(result_data, test_data):
    question_count = len(test_data.questions)
    correct_answers = 0
    del result_data['test_results']
    for question_id, answer_id in result_data.items():
        for question in test_data.questions:
            if int(question.question_id) == int(question_id):
                for answer in question.answers:
                    if int(answer.id) == int(answer_id):
                        if answer.true_answer:
                            correct_answers += 1
    result = correct_answers * 100 / question_count
    return int(result)


@app.route('/maintest', methods=['GET', 'POST'])
def maintest():
    if request.method == 'POST':
        result_data = request.form.to_dict()
        result_information = check_results(result_data, test)
        return render_template('result.html', result_information=result_information)

    return render_template('test.html', test=test)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run()
