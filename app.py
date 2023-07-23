from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user, logout_user, LoginManager, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from models.databasemanager import DatabaseManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True

    app.config['SECRET_KEY'] = 'secret-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    return app


app = create_app()
app.app_context().push()

test = DatabaseManager().get_test('15 Minutes Test')
vocabulary_test = DatabaseManager().get_test('Commonly Misspelled Words')
grammar_test = DatabaseManager().get_test('Grammar')


@app.route('/')
def index():
    return render_template('idex.html')


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


def create_user_score(user_id, test_id, score):
    from models.user_score import UserScore
    user_score = UserScore.query.filter_by(test_id=int(test_id), user_id=int(user_id)).first()
    if user_score:
        user_score.score = int(score)
    else:
        new_user_score = UserScore(user_id=int(user_id), test_id=int(test_id), score=int(score))
        db.session.add(new_user_score)
    db.session.commit()


@app.route('/maintest', methods=['GET', 'POST'])
def main_test():
    if request.method == 'POST':
        result_data = request.form.to_dict()
        result_information = check_results(result_data, test)
        if current_user.is_authenticated:
            create_user_score(current_user.id, test.id, result_information)

        return render_template('result.html', result_information=result_information)
    return render_template('test.html', test=test)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/vocabulary', methods=['GET', 'POST'])
def vocabulary():
    if request.method == 'POST':
        result_data = request.form.to_dict()
        result_information = check_results(result_data, vocabulary_test)
        if current_user.is_authenticated:
            create_user_score(current_user.id, vocabulary_test.id, result_information)

        return render_template('result.html', result_information=result_information)
    return render_template('test.html', test=vocabulary_test)


@app.route('/grammar', methods=['GET', 'POST'])
def grammar():
    if request.method == 'POST':
        result_data = request.form.to_dict()
        result_information = check_results(result_data, grammar_test)
        if current_user.is_authenticated:
            create_user_score(current_user.id, grammar_test.id, result_information)

        return render_template('result.html', result_information=result_information)
    return render_template('test.html', test=grammar_test)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    from models.user import User

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    from models.user import User

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    from models.user_score import UserScore
    user_scores = UserScore.query.filter_by(user_id=int(current_user.id)).all()
    made_test = {}
    if len(user_scores) > 0:
        for user_score in user_scores:
            test_name = DatabaseManager().get_test_name(user_score.test_id)
            made_test[test_name] = user_score.score

    return render_template('profile.html', username=current_user.name, made_test=made_test)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('idex.html')


if __name__ == '__main__':
    app.run()
