import requests
from .file_handler import load_thread_file, load_media_file


class Status:
    def __init__(self, tweet, paths):
        self.tweet = tweet
        self.paths = paths
        medias = list(map(lambda e: load_media_file(e), paths))
        self.uploaded_medias = {}
        for media in medias:
            post_form_data = requests.get('https://api.threadedtweeter.com/upload').json()
            files={'file': media}
            post_res = requests.post(post_form_data['url'], data=post_form_data['fields'], files=files)
            self.uploaded_medias[media.name] = post_form_data['fields']['key']
    def convert_to_dict(self):
        return {
            'STATUS': self.tweet,
            'MEDIA': self.uploaded_medias
        }
