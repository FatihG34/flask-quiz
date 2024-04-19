from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#? SQLite veritabanı konfigürasyonu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
db = SQLAlchemy(app)

#? Veritabanı modeli
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)

#? Tablo oluştur
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    # global highest_score
    
    if request.method == 'POST':
        #? Formdan gelen verileri al
        username = request.form['username']
        question1 = request.form['question1']
        question2 = request.form['question2']
        question3 = request.form['question3']

        
        #? Puanı hesapla (örneğin, basitçe form elemanlarının toplamı olarak)
        score = len(username) + len(question1) +len(question2) + len(question3)

        #? Uygulama bağlamı oluştur
        with app.app_context():
            #? Veritabanına kaydet
            db.session.add(Score(score=score))
            db.session.commit()
        
  

        #? Tüm skorları al ve en yükseğini bul
    with app.app_context():
        highest_score = db.session.query(db.func.max(Score.score)).scalar()
    
    return render_template('quiz.html', highest_score=highest_score)

if __name__ == '__main__':
    app.run(debug=True)
