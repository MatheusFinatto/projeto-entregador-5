from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/top-games')
def top_games():
    return render_template('top-games.html')


if __name__ == '__main__':
    app.run(debug=True)
