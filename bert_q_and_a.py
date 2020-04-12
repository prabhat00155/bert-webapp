from flask import ( 
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
)
import json
import requests

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/predict')
def predict():
    service_url = 'http://07ae7da0-5dbc-427a-a933-67d72ba15a81.uksouth.azurecontainer.io/score'
    question = session.get('question', None) 
    answer_text = session.get('answer_text', None) 
    test_sample = json.dumps({
        'question': [question],
        'answer_text': [answer_text] 
    })
    test_sample = bytes(test_sample, encoding = 'utf8')
    headers = {'Content-Type':'application/json'}
    labels = []
    resp = requests.post(service_url, test_sample, headers=headers)
    label = resp.text.split(',')[0].split(':')[-1].strip(' \"')
    return render_template(
        'result.html', question=question, answer_text=answer_text,
        label=label)

@app.route('/', methods=['POST'])
def upload_question():
    if request.method == 'POST':
        if 'question' not in request.form:
            flash('No file part')
            return redirect(request.url)
        answer_text = request.form['answer_text']
        question = request.form['question']
        if answer_text == '' or question == '':
            flash('No answer_text or question entered for uploading')
            return redirect(request.url)
        session['answer_text'] = answer_text 
        session['question'] = question 
        flash('Question submitted successfully')
        return redirect('/predict') 
