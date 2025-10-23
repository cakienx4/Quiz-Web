from flask import Flask, redirect, request, render_template, url_for
import json, os
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
        option_A = request.form['option_A']
        option_B = request.form['option_B']
        option_C = request.form['option_C']
        option_D = request.form['option_D']
        correct_answer = request.form['correct_answer']

        new_question = {
            'question': question,
            'options': {
                'A': option_A,
                'B': option_B,
                'C': option_C,
                'D': option_D
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
        index = int(request.form['question_index'])
        if 0 <= index < len(questions):
            questions.pop(index)
            save_questions(questions)
            return redirect(url_for('admin_dashboard'))
        else:
            return "Chỉ số câu hỏi không hợp lệ!", 400


    return render_template('delete_question.html')

if __name__ == '__main__':
    app.run(debug=True)