from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



# In-memory storage for surveys and responses
surveys = []
responses = {}

@app.route('/')
def index():
    return render_template('index.html', surveys=surveys)

@app.route('/create', methods=['GET', 'POST'])
def create_survey():
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        surveys.append({'title': title, 'question': question, 'id': len(surveys)})
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
def take_survey(survey_id):
    survey = next((s for s in surveys if s['id'] == survey_id), None)
    if not survey:
        return "Survey not found!", 404

    if request.method == 'POST':
        answer = request.form['answer']
        if survey_id not in responses:
            responses[survey_id] = []
        responses[survey_id].append(answer)
        return redirect(url_for('results', survey_id=survey_id))

    return render_template('survey.html', survey=survey)

@app.route('/results/<int:survey_id>')
def results(survey_id):
    survey = next((s for s in surveys if s['id'] == survey_id), None)
    if not survey:
        return "Survey not found!", 404

    survey_responses = responses.get(survey_id, [])
    return render_template('results.html', survey=survey, responses=survey_responses)

if __name__ == '__main__':
    app.run(debug=True)
