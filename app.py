from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
from extensions import db
from models import Question, User
from models import User, Question
from flask import Flask, render_template, redirect, request, session, url_for
from extensions import db
from models import Question, User

app = Flask(__name__)
app.secret_key = SECRET_KEY_HERE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# 🔽 Veritabanını başlatmak için context içinde tablo ve veri oluşturma
with app.app_context():
    db.create_all()
    if not Question.query.first():
        questions = [
            Question(
                text="Discord.py ile sohbet botu nasıl başlatılır?",
                correct_answer="client.run(TOKEN)",
                options=["app.run()", "TOKEN.start()", "client.run(TOKEN)", "bot.begin()"]
            ),
            Question(
                text="Flask nedir?",
                correct_answer="Python web framework'üdür.",
                options=["Veritabanıdır", "Python modülü değildir", "CSS kütüphanesidir", "Python web framework'üdür."]
            ),
            Question(
                text="Yapay zeka algoritmalarında en çok kullanılan kütüphane?",
                correct_answer="TensorFlow",
                options=["Flask", "BeautifulSoup", "TensorFlow", "NLTK"]
            ),
            Question(
                text="Computer Vision için kullanılan kütüphane?",
                correct_answer="ImageAI",
                options=["BeautifulSoup", "FlaskAI", "ImageAI", "SpeechAI"]
            ),
            Question(
                text="Doğal Dil İşleme için kullanılan kütüphane?",
                correct_answer="NLTK",
                options=["NumPy", "Matplotlib", "NLTK", "Pandas"]
            )
        ]
        db.session.add_all(questions)
        db.session.commit()

@app.route("/", methods=["GET", "POST"])
def quiz():
    questions = Question.query.all()
    total_q = len(questions)

    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username

        # Kullanıcıyı oluştur veya getir
        user = User.query.filter_by(name=username).first()
        if not user:
            user = User(name=username)
            db.session.add(user)
            db.session.commit()

        # Skor hesaplama
        score = 0
        for q in questions:
            if request.form.get(str(q.id)) == q.correct_answer:
                score += 1

        score = score / total_q * 100
        user.last_score = score
        if score > user.high_score:
            user.high_score = score
        db.session.commit()

        session["score"] = score
        return redirect(url_for("result"))

    return render_template("quiz.html", questions=questions)


@app.route("/result")
def result():
    username = session.get("username")
    user = User.query.filter_by(name=username).first()
    max_score = db.session.query(db.func.max(User.high_score)).scalar()

    return render_template("result.html", user=user, max_score=max_score)


if __name__ == "__main__":
    app.run(debug=True)

