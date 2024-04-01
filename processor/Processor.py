from PIL import Image, ImageFont, ImageDraw
import requests
import io



def createPostImage(response: str, backgroundURI: str):
    """ Creates a post with the response to be uploaded to Instagram 
    
    Parameters:
    (str)response: The raw response from the google form
    (str)backgroundURI: The URI for the background photo
    
    """
    response = requests.get(backgroundURI) # Get the image
    img = Image.open(io.BytesIO((response.content)))

    # Make the image dimmer
    mask = Image.new("RGBA", img.size, (0, 0, 0, 160))
    img.paste(mask, (0, 0), mask)

    # Make draw object
    draw = ImageDraw.Draw(img)

    # Add the Dancing Script text first
    dancingScriptFont = ImageFont.truetype("./fonts/DancingScript.ttf", 50)

    draw.text((20, 20), "Make someone smile; Say something kind:", fill=(255, 255, 255), font=dancingScriptFont)
    draw.text((21, 20), "Make someone smile; Say something kind:", fill=(255, 255, 255), font=dancingScriptFont) # Makes it a little bolder since the bold font is not supported by PIL

    

    img.show()



if __name__ == "__main__":
    createPostImage("You are loved and I hope you had a very happy day indeed. Spring break was very fun and I hope you enjoyed it!",
                    "https://images.unsplash.com/photo-1678791564760-725c8798f458?ixid=M3w1ODU1ODV8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MTE5MzE1NDZ8&ixlib=rb-4.0.3?w=1080&h=1080&fit=crop")