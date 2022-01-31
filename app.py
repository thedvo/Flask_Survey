from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def show_start():
    """Generates start survey page"""
    title = survey.title
    instructions = survey.instructions

    return render_template('start.html', title=title, instructions=instructions)


@app.route('/start', methods=['POST'])
def start_survey():
    """Empty responses list. Starts survey and redirects to first question."""
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/questions/<int:id>')
def show_question(id):
    """Renders questions based on their ID"""
    responses = session.get('responses')
    # redirects to home page if response list is empty, meaning survey has not started
    if (responses is None):
        return redirect('/')

    # if the length of the response list is equal to the length of the questions list, survey is complete.
    if (len(responses) == len(survey.questions)):
        return redirect('/done')

    # if the user enters an invalid question ID into the URL, it will flash a message and redirect to the correct route
    if (len(responses) != id):
        flash(
            f"Invalid question id: {id}. Please enter a valid question number.")

        return redirect(f"questions/{len(responses)}")

    # if none of those conditionals are met, survey continues in progress. Shows question on page.
    question = survey.questions[id]

    return render_template('questions.html', question=question, question_num=id)


@app.route('/answer', methods=['POST'])
def handle_questions():
    """Collects user responses to questions"""

    choice = request.form['answer']

    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses


    """Checking length of responses list to determine next route"""
    if (len(responses) == len(survey.questions)):
        return redirect('/done')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/done')
def show_thanks():
    """Shows thank you message to user once survey is complete"""
    return render_template('completed.html')
