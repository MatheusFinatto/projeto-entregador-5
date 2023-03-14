from flask import Flask
from routes_functions import top_games, index

app = Flask(__name__)

app.add_url_rule('/top-games', view_func=top_games.top_games)
app.add_url_rule('/', view_func=index.index)


if __name__ == '__main__':
    app.run(use_reloader=True)
