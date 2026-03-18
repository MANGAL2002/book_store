from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="nu_bookstore_db"
)

@app.route('/')
def home():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    new_books = [b for b in books if b['is_new'] == 1]

    return render_template("home.html", books=books, new_books=new_books)


@app.route('/book/<int:id>')
def book_detail(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cursor.fetchone()

    return render_template("book_detail.html", book=book)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        is_new = request.form.get('is_new') == 'on'

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO books (title, category, description, is_new) VALUES (%s,%s,%s,%s)",
            (title, category, description, is_new)
        )
        db.commit()

        return redirect('/')

    return render_template("add_book.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)