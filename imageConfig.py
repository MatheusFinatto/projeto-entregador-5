# troca a resolução das imagens que vem da IGDB
def coverConfig(response):
    # response.json() é um array de objetos (url de imagens)
    newJson = []
    newJson = {"data": response.json().copy()}
    for i in range(len(response.json())):
        if 'cover' in newJson["data"][i]:
            newJson["data"][i]['cover']["url"] = response.json(
            )[i]['cover']["url"].replace("t_thumb", "t_1080p")
    return newJson


# troca a resolução das imagens que vem da IGDB
def artworkConfig(response):
    # response.json() é um array de objetos (url de imagens)
    newJson = response.copy()
    if 'artworks' in response["data"][0]:
        for i in range(len(response['data'][0]['artworks'])):
            newJson['data'][0]['artworks'][i]['url'] = response['data'][0]['artworks'][i]['url'].replace(
                "t_thumb", "t_1080p")
    return newJson
