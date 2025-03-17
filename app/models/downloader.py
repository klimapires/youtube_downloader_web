from pytube import YouTube
from tqdm import tqdm
import os
import urllib.request

# Função para atualizar os cabeçalhos HTTP
def update_headers():
    opener = urllib.request.build_opener()
    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )
    ]
    urllib.request.install_opener(opener)

class YouTubeDownloader:
    def __init__(self, url, output_path, quality):
        self.url = url
        self.output_path = output_path
        self.quality = quality

    def download(self):
        # Atualiza os cabeçalhos HTTP antes de fazer o download
        update_headers()

        yt = YouTube(self.url)
        stream = yt.streams.filter(res=self.quality, file_extension='mp4').first()
        if not stream:
            raise ValueError(f"No stream found with quality {self.quality}")

        total_size = stream.filesize
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
            stream.download(output_path=self.output_path, filename='temp_video.mp4')
            pbar.update(total_size)

        return os.path.join(self.output_path, 'temp_video.mp4')