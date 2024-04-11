from instagrapi import Client
import logging
from . import cached_instagram_accs



logger = logging.getLogger("instagram")

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
        logger.info("Uploading post to instagram")
        self.cl.photo_upload(
            path=imagePath,
            caption=caption
        )

def getInstagram(school: str, accountCreds: dict) -> Instagram:
    """ Gets the appropriate instagram account session 
    
    Parameters:
    (str)school: The name of the school to identify the account
    (dict)accountCreds: A dictionary with with account credentials assigned to the school name identifier

    Returns:
    (Instagram): An instance of the instagram account
    
    """
    if (school in cached_instagram_accs):
        logger.info("Returning cached IG login for school: %s" % school)
        return cached_instagram_accs[school]

    # Login to account and add to bot.ig
    logger.info("Logging into IG for school: %s" % school)
    creds = accountCreds[school]['instagram']
    igAcc = Instagram(creds['username'], creds['password'])
    cached_instagram_accs[school] = igAcc
    return igAcc