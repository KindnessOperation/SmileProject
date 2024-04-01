from PIL import Image
import requests
import io



def createPostImage(response: str, backgroundURI: str):
    """ Creates a post with the response to be uploaded to Instagram 
    
    Parameters:
    (str)response: The raw response from the google form
    (str)backgroundURI: The URI for the background photo
    
    """
    while True:
        response = requests.get(backgroundURI) # Get the image
        img = Image.open(io.BytesIO((response.content)))

        # Make the image dimmer
        mask = Image.new("RGBA", img.size, (0, 0, 0, int(input())))
        img.paste(mask, (0, 0), mask)

        img.show()



if __name__ == "__main__":
    createPostImage("You are loved and I hope you had a very happy day indeed. Spring break was very fun and I hope you enjoyed it!",
                    "https://images.unsplash.com/photo-1678791564760-725c8798f458?ixid=M3w1ODU1ODV8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MTE5MzE1NDZ8&ixlib=rb-4.0.3?w=1080&h=1080&fit=crop")