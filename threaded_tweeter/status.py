import requests
from .file_handler import load_thread_file, load_media_file
from .config import THREADED_TWEETER_URL


S3_BASE_URL = 'https://s3.amazonaws.com/threadtweeter-media'

class Status:
    def __init__(self, tweet, paths):
        self.tweet = tweet
        self.paths = paths
        self.medias = list(map(lambda e: load_media_file(e), paths))
        self.uploaded_medias = []
    def upload_media_to_s3(self):
        for media in self.medias:
            post_form_data = requests.get(f'{THREADED_TWEETER_URL}/upload').json()
            files={'file': media}
            post_res = requests.post(post_form_data['url'], data=post_form_data['fields'], files=files)
            self.uploaded_medias.append(f'{S3_BASE_URL}/{post_form_data["fields"]["key"][:-12]}/{media.name}')
    def convert_to_dict(self):
        return {
            'STATUS': self.tweet,
            'MEDIA': self.uploaded_medias
        }
    def __str__(self):
        return f'Status: {self.tweet}\nImage: {self.paths}'