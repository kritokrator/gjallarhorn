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
