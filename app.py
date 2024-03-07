from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey

from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def start_survey():
    # Reset the session at the start of the survey
    session['responses'] = []
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/begin', methods=['POST'])
def begin_survey():
    # Initialize session responses to empty list when survey begins
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get('responses')
    # Redirect to thank you page if all questions have been answered
    if responses is None:
        return redirect('/')
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    # Redirect to current question if out of order access is attempted
    if len(responses) != qid:
        flash("You're trying to access an invalid question.")
        return redirect(f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question_num=qid, question=question)

@app.route('/answer', methods=['POST'])
def handle_answer():
    # Retrieve the current list of responses from the session, or initialize it if not present
    responses = session.get('responses', [])
    # Get the new answer from the form submission
    new_answer = request.form['answer']
    # Append the new answer to the responses list
    responses.append(new_answer)
    # Update the session with the new list of responses
    session['responses'] = responses

    # Determine the next step: redirect to the next question or finish the survey
    if len(responses) < len(satisfaction_survey.questions):
        # Redirect to the next question
        return redirect(f'/questions/{len(responses)}')
    else:
        # All questions answered, redirect to the thank you page
        return redirect('/thankyou')


@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')








