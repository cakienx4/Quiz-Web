from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/answer_question', methods=['GET', 'POST'])
def answer_question():
    if request.method == 'POST':
        # Xử lý câu trả lời ở đây
        pass
    return render_template('answer_question.html')

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
        # Xử lý thêm câu hỏi ở đây
        pass
    return render_template('add_question.html')

@app.route('/delete_question', methods=['GET','POST'])
def delete_question():
    if request.method == 'POST':
        # Xử lý xóa câu hỏi ở đây
        pass
    return render_template('delete_question.html')

if __name__ == '__main__':
    app.run(debug=True)