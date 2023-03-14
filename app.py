import requests
from flask import Flask, render_template,  jsonify

app = Flask(__name__)

# function que checa se a url da imagem existe... talvez seja necessária no futuro
# def check_image(url):
#     response = requests.get(url)
#     status = response.status_code
#     if status != 200:
#         url = url.replace("t_720p", "t_1080p")
# check_image(f"http:{cover_url}")

HEADERS = {
    'Client-ID': 'tvpgyurlv8vc88kd9dzum9s0ldlbf2',
    'Authorization': 'Bearer f1fzl61lle5vii2zwca6x2ghswne5z',
    'Content-Type': 'application/json',
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/top-games')
def top_games():
    url = 'https://api.igdb.com/v4/covers'
    data = f'fields url, game.name; limit 50;'
    headers = HEADERS
    response = requests.post(url, headers=headers, data=data)
    newJson = []
    if response.ok:
        # response.json() é um array de objetos (url de imagens)
        newJson = response.json().copy()
        for i in range(len(response.json())):
            newJson[i]["url"] = response.json(
            )[i]['url'].replace("t_thumb", "t_1080p")

        return render_template('top-games.html', newJson=newJson)
    else:
        return jsonify({'error': 'Failed to retrieve game cover.'}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
