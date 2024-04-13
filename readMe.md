# Smile Project


## Description
Smile Project is a project that posts kind messages made by the community on an Instagram page through an anonymous Google Form. The messages are then placed on a template with a randomized picture of a flower in the background, creating a neatly designed post. This project's goal was to help make the creation of posts autonomous with small intervention to approve posts and responses all integrated through Discord.

## How it works
1. Google Form responses are sent in a discord channel
2. The owner can approve responses to be posted
3. A various selection of background images can be selected for the post (Cycle images by selecting the X)
4. If approved, the bot will post the image on Instagram

## Installation
To install the dependencies required for Smile Project use:

```pip install -r requirements.txt```

Create a file called ```token.json``` with an empty json dictionary inside; This is where credentials will be stored.

### Setup Google Application
Setup an application to auth with the bot with [Google Cloud](https://developers.google.com/workspace/guides/get-started). This app is used to authenticate with the Google API with OAUTH2.
- Enable the [Forms API](https://console.cloud.google.com/flows/enableapi?apiid=forms.googleapis.com)
- Add a service account to the app and download as ```service_account.json```
- Add the account with the Google Forms into the testing user list

### Google Form
Setup a Google Form with one question. Note: Question must be text-based, typically a long answer box.
- **IMPORTANT**: The first question is where the response is extracted. All other questions are ignored
- Record the Google Form ID in ```config.json```
- Account with Google Form must be authorized as a test user in the OAUTH2 Application
    - When first running the program, you must authorize the app to have access to the forms. Note: This is only needed once and login is cached afterwards in ```token.json```


## Configuration
The bot can manage multiple accounts and forms at once. ```config.json``` contains the configuration files required to run the program.
- ### unsplashAccessToken
    - An unsplash token is required to fetch background images. [Unsplash](https://unsplash.com/developers) provides documentation on how to generate an API key
- ### discordToken
    - A token for a discord bot is required so that responses/posts can be approved by the owner. [Discord Application Portal](https://discord.com/developers/applications)
    - All intents must be enabled for the bot to work correctly
- ### webhook
    - A webhook URL is required to send responses from the Google Form
- ### channels
    - 3 Channel IDs consisting of:
        - responses: The channel ID where responses are sent. Also the channel with the webhook URL
        - verify: The channel ID where background images are verified
        - success: The channel ID where posts that have been uploaded are recorded
- ### imageQuery
    - The topic of the background images retrieved from Unsplash. Ex: nature, flowers
- ### accounts
    - A dictionary of various accounts that the bot manages
        - The key is the nickname of the account
        - The value is a dictionary with:
            - FormId from Google Forms
            - Dictionary with credentials for the instagram account

## Usage
There are two main files: main.py and bot.py. Both must be ran seperately to make the bot work
```
python main.py
python bot.py
````
Main manages the Google Form and sends responses. Bot manages the response verification, image generation, and posting.

## License
[MIT](https://github.com/TheWalkingSea/SmileProject/blob/main/LICENSE)