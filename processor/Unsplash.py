import requests

class Unsplash:
    def __init__(self, accessToken: str) -> None:
        self.accessToken = accessToken

    def getRandomImage(self, query: str) -> str:
        """ Returns a link with a random photo related to the query; In Instagram post format (1080px x 1080px); Uses unsplash API
        
        Parameters:
        (str)query: What the image will be related to

        Returns:
        (str): A link to the image (1080px x 1080px)

        """
        params = {
            "client_id": self.accessToken,
            "orientation": "squarish",
            "count": 1,
            "query": query
        }
        # Call to API to get a random image with the query
        response = requests.get("https://api.unsplash.com/photos/random", params=params)
        js = response.json()
        return js[0]['urls']['raw'] + "?w=1080&h=1080&fit=crop" # Parameters to make it fit in an Instagram post

if __name__ == "__main__":
    import json
    with open("./config.json") as f:
        js = json.load(f)
        print(Unsplash(js['unsplashAccessToken']).getRandomImage("flowers"))