from flask import Flask, redirect, request, render_template, url_for
import json, os
import ast

app = Flask(__name__)

data_file = 'data/questions_data.json'

def load_questions():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_questions(questions):
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)

questions = load_questions()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/answer_question', methods=['GET', 'POST'])
def answer_question():
    if not questions:
        return render_template('none_question_homeType.html')
    if request.method == 'POST':
        answer = {}
        for i, _ in enumerate(questions):
            answer[i] = request.form.get(f'question_{i}')
        return render_template('result.html', answers = str(answer))
    return render_template('answer_question.html', questions=questions)

@app.route('/check_admin', methods=['POST'])
def check_admin():
    password = request.form.get('ma-admin')
    if password == 'admin123':
        return redirect(url_for('admin_dashboard'))
    else:
        return "Mật khẩu sai!", 403
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/add_question', methods=['GET','POST'])
def add_question():
    if request.method == 'POST':
        question = request.form['question']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_answer = request.form['correct_answer']

        new_question = {
            'question': question,
            'options': {
                'A': option_a,
                'B': option_b,
                'C': option_c,
                'D': option_d
            },
            'correct_answer': correct_answer
        }

        questions.append(new_question)
        save_questions(questions)

        return redirect(url_for('admin_dashboard'))
    return render_template('add_question.html')

@app.route('/delete_question', methods=['GET','POST'])
def delete_question():
    if not questions:
        return render_template('none_question_adminType.html')

    if request.method == 'POST':
        index = request.form.get('question_index')
        if index is not None:
            index = int(index)
            if 0 <= index < len(questions):
                del questions[index]
                save_questions(questions)
        return redirect(url_for('delete_question'))
    
    return render_template('delete_question.html', questions=questions)

@app.route('/result')
def result():
    answers = ast.literal_eval(request.args.get('answers'))
    # ép key về int
    answers = {int(k): v for k, v in answers.items()}

    correct = 0
    for i, q in enumerate(questions):
        if answers.get(i) == q['correct_answer']:
            correct += 1

    correct = round((correct / len(questions)) * 100, 2)
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)