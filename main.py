import requests
import json
from googleapiclient.discovery import build
import settings

class Downloader():

    def __init__(self, user, api_key):
        self.user = user
        self.api_key = api_key

    def get_first_page(self):
        url = 'http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={}&api_key={}&page={}&format=json'.format(
            self.user, self.api_key, 1)
        response = requests.get(url)
        page = json.loads(response.text)
        self.total_pages = int(page['lovedtracks']['@attr']['totalPages'])
        return page['lovedtracks']['track']

    def get_page(self, page_nr):
        url = 'http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={}&api_key={}&page={}&format=json'.format(
            self.user, self.api_key, page_nr)
        response = requests.get(url)
        page = json.loads(response.text)
        return page['lovedtracks']['track']

    def get_all_tracks(self):
        result = self.get_first_page()
        for page_nr in range(2, self.total_pages + 1):
            url = 'http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={}&api_key={}&page={}&format=json'.format(
                'DoomhammerNG', '28f67b370f7edbeb924d6bfac6c0dcce', page_nr)
            response = requests.get(url)
            page = json.loads(response.text)
            result += page['lovedtracks']['track']
        return result


class LinkGatherer:

    max_results_from_youtube = 5

    def __init__(self, track_list, developer_key):
        self.track_list = track_list
        self.DEVELOPER_KEY = developer_key
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'

    def get_links(self):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY)
        videos = {}
        youtube_link_base = 'https://www.youtube.com/watch?v={}'
        for track in self.track_list:
            query = '{} {}'.format(track['name'], track['artist']['name'])
            search_response = youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=self.max_results_from_youtube
            ).execute()
            videos[track['artist']['name']] = []
            for search_result in search_response.get('items', []):
                if search_result['id']['kind'] == 'youtube#video':
                    youtube_single_result = {
                        'title': search_result['snippet']['title'],
                        'link': youtube_link_base.format(search_result['id']['videoId'])
                    }
                    videos[track['artist']['name']].append(youtube_single_result)
        return videos

if __name__ == '__main__':
    user = 'DoomhammerNG'

    last_fm_downloader = Downloader(user=user, api_key=settings.api_key)

    with open('last_fm_json.json') as f:
        result = json.load( f)
    print(len(result))
    youtube_link_gatherer = LinkGatherer(result, settings.youtube_gjallarhorn_api_key)
    videos = youtube_link_gatherer.get_links()
    with open('youtube_results.json', 'w') as f:
        json.dump(videos, f)
    print(videos)
