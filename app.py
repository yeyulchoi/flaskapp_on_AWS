from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector


app = Flask(__name__)
#Old sqlite db.
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flaskaws.db'
#new mysql db.
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/flask_aws2'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return f"Book(Title:{self.title}, author:{self.author}, price:{self.price}.)"



@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    if request.method =='POST':
        book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            price=request.form.get('price'))
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))



if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)