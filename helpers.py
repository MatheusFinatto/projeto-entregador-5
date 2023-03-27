def coverConfig(response):
    # response.json() é um array de objetos (url de imagens)
    newJson = []
    newJson = {"data": response.json().copy()}
    for i in range(len(response.json())):
        if 'cover' in newJson["data"][i]:
            newJson["data"][i]['cover']["url"] = response.json(
            )[i]['cover']["url"].replace("t_thumb", "t_1080p")
    return newJson
