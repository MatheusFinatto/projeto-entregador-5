from flask import jsonify, render_template
import requests

HEADERS = {
    'Client-ID': 'tvpgyurlv8vc88kd9dzum9s0ldlbf2',
    'Authorization': 'Bearer f1fzl61lle5vii2zwca6x2ghswne5z',
    'Content-Type': 'application/json',
}


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
