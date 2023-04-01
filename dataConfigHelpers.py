from flask import session
from databaseFunctions import get_db_connection

# troca a resolução das capas dos jogos,  que vem da IGDB, para fullHD


def newJsonGenerator(json):
    if not isinstance(json, dict) or not json['data']:
        return {"data": json.copy()}
    return json.copy()


def imageConfig(response, imgType):
    # response.json() é um array de objetos (url de imagens)
    if (imgType == 'cover'):
        newJson = newJsonGenerator(response.json())
        for i in range(len(response.json())):
            if 'cover' in newJson["data"][i]:
                newJson["data"][i]['cover']["url"] = response.json(
                )[i]['cover']["url"].replace("t_thumb", "t_1080p")
        return newJson
    else:
        newJson = newJsonGenerator(response)
    if 'artworks' in response["data"][0]:
        for i in range(len(response['data'][0]['artworks'])):
            newJson['data'][0]['artworks'][i]['url'] = response['data'][0]['artworks'][i]['url'].replace(
                "t_thumb", "t_1080p")
    return newJson


# def setFavorites(game_id):
#     addFavoriteDB(session.get("id"), game_id)
#     return 'Foi'


def getFavorites(response):
    # checa se o usuario está logado
    if (session.get("username")):
        # cria conexão
        conn = get_db_connection()

        # faz uma copia da query de games
        newJson = response.copy()

        # busca os favoritos do usuário da db
        cur = conn.cursor()
        user_id = session.get("id")
        cur.execute("SELECT game_id FROM favorites WHERE user_id=?", [user_id])
        favorites = cur.fetchall()

        # itera sobre os jogos vindos da API e verifica se seus id's foram marcados como favoritos
        for i in range(len(response['data'])):
            for j in range(len(favorites)):
                is_favorite = response["data"][i]['id'] in favorites[j]
                newJson['data'][i]['isFavorite'] = is_favorite
                if is_favorite:
                    break
        return newJson


# def setWishlist(response):
#     print("WORKS")
#     newJson = response.copy()
#     for i in range(len(response['data'])):
#         is_wished = response["data"][i]['id'] in wished
#         newJson['data'][i]['isWished'] = is_wished
#     return newJson

def getWishlist(response):
    # TODO MUDA OS NOME MATHEUS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # checa se o usuario está logado
    if (session.get("username")):
        # cria conexão
        conn = get_db_connection()

        # faz uma copia da query de games
        newJson = response.copy()

        # busca os favoritos do usuário da db
        cur = conn.cursor()
        user_id = session.get("id")
        cur.execute("SELECT game_id FROM favorites WHERE user_id=?", [user_id])
        favorites = cur.fetchall()

        # itera sobre os jogos vindos da API e verifica se seus id's foram marcados como favoritos
        for i in range(len(response['data'])):
            for j in range(len(favorites)):
                is_favorite = response["data"][i]['id'] in favorites[j]
                newJson['data'][i]['isFavorite'] = is_favorite
                if is_favorite:
                    break
        return newJson
