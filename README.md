# Gjallarhorn

This is a tool for gathering information about specific user's favourite tracks from a third-party site,
and collecting youtube links for each of the favourite tracks.

Currently only one user is supported, and his last.fm username is hardcoded in the project, also the only supported data provider is last.fm.

## Prerequisites

### Python version

This project was developed using python `3.6.4`. Other versions were not tested.

### Additional libraries

Additional dependecies are included in the `requirements.txt` file. Install them using `pip` or any other way you choose.
If you plan on using pip: `pip install -r requirements.txt` should be enough.

### Additional resources

This project currently uses two outside sources for data: last.fm and youtube.

From last fm, you need to get the api_key and api_secret for your account.
For a broad overview on how to accuire them go [here](https://www.last.fm/api/authentication)

Once you get them place them in a file `settings.py` (you may need to create it by hand in the project root) in respective variables:

    api_key = ''
    api_secret = ''

On youtube, you will need to create your own application with access to youtube api. Good place to start checking how to do that
is [here](https://developers.google.com/youtube/v3/). Once you create your app with access to youtube api service,
initialise the following variables with respective information, and place them in `settings.py` file in the root of the project:

    application_name = ''
    application_owner = ''
    youtube_gjallarhorn_api_key = ''

## Usage

As mentiond before, currently only one user is supported, and his last.fm username is hardcoded in the project,
also the only supported data provider is last.fm.

To get links to his favourite tracks simply call the main script:

`python main.py`

The results will be saved in a json format in a file `youtube_results.json` saved inside the project root.

# README asatumpost

Small project allowing user to automate posting tasks from Asana to Tumblr.

## How to get started

### Install requirements

Project was written using Python 3.5.2, but should work on other versions as well.

In order to install required packages:  
`pip install -r requirements.txt`

### Get personal access token from Asana

1. On your Asana account go to "My Profile Settings".
2. Go to "Apps" tab and click on "Manage developer apps".
3. Click on "Create new personal access token" and generate one.
4. Export it as your environmental variable or add to `.env` file managed by
   `direnv`:  
```bash
export ASANA_PERSONAL_ACCESS_TOKEN="your_personal_access_token"
```

### Authorize this app on your Tumblr account

1. Register this app on [Tumblr](https://www.tumblr.com/oauth/apps)
using `http://localhost` as callback URL.
2. Export your OAuth Consumer Key and Consumer Secret as environmental
variables:  
```bash
export TUMBLR_CONSUMER_KEY="your_consumer_key"
export TUMBLR_CONSUMER_SECRET="your_consumer_secret"
```
3. Go to [API console](https://api.tumblr.com/console) and put consumer
key and secret in order to get OAuth token and secret.
4. Export new information as environment variables as well:  
```bash
export TUMBLR_OAUTH_TOKEN="your_oauth_token"
export TUMBLR_OAUTH_SECRET="your_oauth_secret"
```

### Provide path to your folder containing task files

Export path of desired directory as environment variable so the app can
scan it and look for new posts:
```bash
export PATH_TO_ASANA_DIRECTORY="your_path"
```

### Usage

In order to run app just type `python main.py` in terminal.
There are three interactions in app:
1. Pick your workspace on Asana, that you would like to import
tasks from.
2. Pick your blog on Tumblr, that you would like to post on.
3. Select if you want to mark the task as done.
