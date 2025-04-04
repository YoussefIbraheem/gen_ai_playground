from flask import Flask , render_template , request , redirect , url_for
import os
from models import Author , Book , Review , db

BASE_DIR = os.path.abspath(os.getcwd())
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'books.db')}"

db.init_app(app=app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.all()
    return render_template("index.html",books=books)

@app.route('/add',methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author']
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author= Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        if title:    
            book = Book(title=title,author_id=author.id)
            db.session.add(book)
            db.session.commit()
        return redirect(url_for('index'))
    else:    
        return render_template("add_book.html")

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_book(id):
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_author = request.form['new_author']
        author = Author.query.filter_by(name=new_author).first()
        if not author:
            author= Author(name=new_author)
            db.session.add(author)
            db.session.commit()
        if new_title:
            book = Book.query.filter_by(id=id).first_or_404()    
            book.title = new_title
            book.author_id = author.id
            db.session.commit()
        return redirect(url_for('index'))
    else:
      book = Book.query.filter_by(id=id).first_or_404()
      return render_template("edit_book.html",book=book)
  
  
  
@app.route('/delete/<int:id>')
def delete_book(id):
     book = Book.query.filter_by(id=id).first_or_404()
     if book:
         db.session.delete(book)
         db.session.commit()
         return redirect(url_for('index'))
              
      
            


if __name__ == "__main__":
    app.run(debug=True)
        
