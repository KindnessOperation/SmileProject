from instagrapi import Client



class Instagram():
    def __init__(self, username: str, password: str) -> None:
        self.cl = Client()
        self.cl.login(username, password)

    def uploadPost(self, imagePath: str, caption: str=None) -> None:
        """ Creates a post with an image path and a caption
        
        Parameters:
        (str)imagePath: A path to the image
        (str)caption: A caption for the post; Defaults to None
        
        """

        self.cl.photo_upload(
            path=imagePath,
            caption=caption
        )