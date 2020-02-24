from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)
#pip install Flask SQLAlchemy flask_sqlalchemy
#set FLASK_APP=server.py
#set FLASK_ENV=development
#flask run

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return f'Title: {self.title}'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.form:
        try:
            book = Book(title = request.form.get('title'))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print('Something went wrong!')
            print(e)
    books = Book.query.all()
    return render_template('home.html', books = books)

@app.route('/update', methods=['POST'])
def update():
    try:
        newtitle = request.form.get('newtitle')
        oldtitle = request.form.get('oldtitle')
        book = Book.query.filter_by(title=oldtitle).first()
        book.title =newtitle
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    try:
        title = request.form.get('title')
        book = Book.query.filter_by(title=title).first()
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect('/')
