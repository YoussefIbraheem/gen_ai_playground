from flask import  render_template , request , redirect , url_for
from models import Author , Book , Review , db
from app import app
from tasks import send_book_notification
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
            send_book_notification.delay(book.id,book.title)
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
              
@app.route('/details/<int:id>')
def book_details(id):
     book = Book.query.filter_by(id=id).first_or_404()
     if book:
         return render_template("book_details.html",book=book)
     
@app.route('/search',methods=['GET','POST'])
def search_book():
    if request.method == 'POST':
        keyword = request.form['keyword']
        books = Book.query.filter(Book.title.ilike(f'%{keyword}%')).all() 
        authors = Author.query.filter(Author.name.ilike(f'%{keyword}%')).all()
        return render_template('search_book.html',books=books,authors=authors)
        
    else:
        return render_template('search_book.html')