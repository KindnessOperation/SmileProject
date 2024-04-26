# The Kindness Operation


## Description
The Kindness Operation is a project that posts kind messages made by the community on an Instagram page through an anonymous Google Form. The messages are then placed on a template with a randomized picture from Unsplash, creating a neatly designed post. This project's goal was to help make the creation of posts autonomous with small intervention to approve posts and responses all integrated through Discord.

## How it works
1. Google Form responses are sent in a discord channel
2. The owner can approve responses to be posted
3. A various selection of background images can be selected for the post (Cycle images by selecting the X)
4. If approved, the bot will post the image on Instagram

## Simple Usage
```
git clone https://github.com/KindnessOperation/TheKindnessOperation.git
cp config/example.config.json config/config.json
// Modify config.json as necessary
// Download client_secrets.json to config/client_secrets.json
docker compose up
```
Main manages the Google Form and sends responses. Bot manages the response verification, image generation, and posting.

### Setup Google Application
Setup a project to allow 2OAuth Flow with the bot using [Google Cloud Console](https://console.cloud.google.com/).
1. Create a project
2. Open the project and setup [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
3. Add gmail account with Google Form to the app (Can be the same email as the owner of the app)
4. Change the app to production to prevent refresh token from expiring ([invalid_grant](https://developers.google.com/google-ads/api/docs/get-started/common-errors))
5. Navigate to [Credentials](https://console.cloud.google.com/apis/credentials) and create an OAuth client ID - Desktop App
6. Download JSON for client secrets to ```config/client_secrets.json```
7. Enable the [Forms API](https://console.cloud.google.com/flows/enableapi?apiid=forms.googleapis.com)

### Authorizing with OAuth2
In order for the bot to connect to the Google Form you must setup the Google Application. If setup, add the user with the google form as a test user and run:
```
python main.py
```
You will be prompted to authorize your account with the bot
- Make sure to login to the account containing the Google Form.
- Credentials will be logged to ```config/token.json```

### Google Form
Setup a Google Form with one question. Note: Question must be text-based, typically a long answer box.
- **IMPORTANT**: The first question is where the response is extracted. All other questions are ignored
- Record the Google Form ID in ```config.json```
- Account with Google Form must be authorized as a test user in the OAuth2 Application
    - When first running the program, you must authorize the app to have access to the forms. Note: This is only needed once and login is cached afterwards in ```token.json```

## Configuration
The bot can manage multiple accounts and forms at once. ```config.json``` contains the configuration files required to run the program.
- ### unsplashAccessToken
    - An unsplash token is required to fetch background images. [Unsplash](https://unsplash.com/developers) provides documentation on how to generate an API key
- ### discordToken
    - A token for a discord bot is required so that the bot can integrate with Discord. [Discord Application Portal](https://discord.com/developers/applications)
        - All intents must be enabled for the bot to work correctly
- ### webhook
    - A webhook URI is required to send responses from the Google Form. Typically a Discord webhook URI from the responses channel
- ### channels
    - 3 Discord Channel IDs consisting of:
        - responses: The channel ID where responses are sent. Also the channel with the webhook URL
        - verify: The channel ID where background images are verified
        - success: The channel ID where posts that have been uploaded are recorded
- ### imageQuery
    - A list of topics for the the background images retrieved from Unsplash. Ex: nature, flowers
- ### accounts
    - A dictionary of various accounts that the bot manages:
        - The key is the nickname of the account
        - The value is a dictionary:
            - FormId from Google Forms
            - Dictionary with credentials for the instagram account

## License
[MIT](https://github.com/KindnessOperation/TheKindnessOperation/blob/main/LICENSE)
