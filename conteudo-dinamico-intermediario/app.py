from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    items = ['item 1', 'item 2', 'item 3']
    return render_template('home.html', items=items, active='home')


@app.route('/games')
def games():
    return render_template('games.html', active='games')


@app.route('/about')
def about():
    return render_template('about.html', active='about')


@app.route('/contact')
def contact():
    return render_template('contact.html', active='contact')


if __name__ == "__main__":
    app.run(ssl_context='adhoc')