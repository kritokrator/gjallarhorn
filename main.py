import requests
import json
from googleapiclient.discovery import build
import settings
from datetime import datetime
from helper import user_select_option

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
        #videos = {}
        youtube_link_base = 'https://www.youtube.com/watch?v={}'
        index = 0
        for track in self.track_list:
            query = '{} {}'.format(track['name'], track['artist']['name'])
            search_response = youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=self.max_results_from_youtube
            ).execute()
            self.track_list[index]['videos'] = []
            videos = self.track_list[index]['videos']
            for search_result in search_response.get('items', []):
                if search_result['id']['kind'] == 'youtube#video':
                    youtube_single_result = {
                        'title': search_result['snippet']['title'],
                        'url': youtube_link_base.format(search_result['id']['videoId'])
                    }
                    videos.append(youtube_single_result)
            index += 1
        return self.track_list


def convert_tracklist_to_semantic_list(tracklist):
    result = []
    for track in tracklist:
        if len(track) > 0 and '-' in track:
            artist, title = map(str.strip, ' '.join(track.split('_')).split('-'))
            result.append({'name': title, 'artist': {'name': artist}})

    return result

def get_blog_name(client):
    client_info = client.info()
    if "meta" in client_info and "status" in client_info["meta"] and client_info["meta"]["status"] == 401:
        print("Your Tumblr credentials seem so fucked up!")
        exit(1)
    blogs = client_info["user"]["blogs"]
    blog_name = user_select_option("Please choose a blog", blogs)["name"]
    return blog_name

def send_videos_to_tumblr_queue(videos):
    import pytumblr
    tum_client = pytumblr.TumblrRestClient(
        settings.TUMBLR_CONSUMER_KEY,
        settings.TUMBLR_SECRET_KEY,
        settings.TUMBLR_OAUTH_TOKEN,
        settings.TUMBLR_OAUTH_SECRET
    )

    for video in videos:
        post_for_tumblr = {'tags': [video['artist']['name']], 'notes': video['videos'][0]['url']}
        blog_name = get_blog_name(tum_client)
        tum_client.create_video(blog_name, state="queue", tags=post_for_tumblr["tags"],
                                embed=post_for_tumblr["notes"])

        stripped_note = post_for_tumblr["notes"].strip()
        posts = tum_client.queue(blog_name)["posts"]
        last_post = posts[-1]
        scheduled_publish_time = last_post["scheduled_publish_time"]
        permalink = last_post["permalink_url"]
        if stripped_note in permalink:
            scheduled_timestamp = datetime.fromtimestamp(int(scheduled_publish_time)).strftime("%Y-%m-%d %H:%M:%S")
            print(
                "Post scheduled for publication at %s on Tumblr" % scheduled_timestamp)
        else:
            print("Shit went wrong!")

download_from_last_fm = False
upload_to_tumblr = True
gather_youtube_info = True

if __name__ == '__main__':
    user = 'DoomhammerNG'

    if download_from_last_fm:
        last_fm_downloader = Downloader(user=user, api_key=settings.api_key)
        result = last_fm_downloader.get_all_tracks()
        with open('last_fm_results.json', 'w') as f:
            json.dump(result, f)

    result = [{'name': 'U-Men', 'artist': {'name': 'Front 242'}}]
    result = convert_tracklist_to_semantic_list(open('list.txt').read().split('\n'))

    if gather_youtube_info:
        youtube_link_gatherer = LinkGatherer(result, settings.youtube_gjallarhorn_api_key)
        videos = youtube_link_gatherer.get_links()
        with open('youtube_results.json', 'w') as f:
            json.dump(videos, f)
    else:
        videos = json.load(open('youtube_results.json'))

    if upload_to_tumblr:
        send_videos_to_tumblr_queue(videos)
