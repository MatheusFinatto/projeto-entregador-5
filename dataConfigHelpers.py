from databaseFunctions import get_db_connection
conn = get_db_connection()

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


# TODO: change placeholder lists for db selects
favorites = [1942, 6036, 1026]
wished = [19560]


def setFavorites(response):
    newJson = response.copy()
    for i in range(len(response['data'])):
        is_favorite = response["data"][i]['id'] in favorites
        newJson['data'][i]['isFavorite'] = is_favorite
    return newJson


# def setFavorites(response):
#     # checa se o usuario está logado
#     if (session == True):

#         # faz uma copia da query de games
#         newJson = response.copy()

#         # busca os favoritos do usuário da db
#         favorites = conn.execute('SELECT * FROM favorites').fetchall()

#         # itera sobre os jogos vindos da API e verifica se seus id's foram marcados como favoritos
#         for i in range(len(response['data'])):
#             is_favorite = response["data"][i]['id'] in favorites
#             newJson['data'][i]['isFavorite'] = is_favorite
#         return newJson


def setWishlist(response):
    print("WORKS")
    newJson = response.copy()
    for i in range(len(response['data'])):
        is_wished = response["data"][i]['id'] in wished
        newJson['data'][i]['isWished'] = is_wished
    return newJson

# def setWishlist(response):
#     # checa se o usuario está logado
#     if (session == True):

#         # faz uma copia da query de games
#         newJson = response.copy()

#         # busca a lista de desejos do usuário da db
#         wished = conn.execute('SELECT * FROM wishlist').fetchall()

#         # itera sobre os jogos vindos da API e verifica se seus id's foram marcados como desejados
#         for i in range(len(response['data'])):
#             is_wished = response["data"][i]['id'] in wished
#             newJson['data'][i]['isFavorite'] = is_wished
#         return newJson
