from flask import Flask, request, render_template
from surveys import Survey, Question, satisfaction_survey

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
responses = []

app.debug = True
app.config['SECRET_KEY'] = "hiii"
debug = DebugToolbarExtension(app)


@app.route('/')
def start_survey():
    return render_template('start.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/questions/<int:question_index>', methods=['GET'])
def show_question(question_index):
    question = satisfaction_survey.questions[question_index]
    return render_template('question.html', question=question, question_index=question_index)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['answer']
    question_index = int(request.form['question_index'])
    responses.append(answer)
    next_question_index = question_index + 1
    if next_question_index < len(satisfaction_survey.questions):
        return redirect(f'/questions/{next_question_index}')
    else:
        return redirect('/thankyou')











