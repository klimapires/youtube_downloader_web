import yt_dlp
import os
import logging
from flask_socketio import emit
from app import socketio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class YouTubeDownloader:
    def __init__(self, url, output_path, quality):
        self.url = url
        self.output_path = output_path
        self.quality = quality

    def progress_hook(self, d):
        """Função chamada pelo yt-dlp para atualizar o progresso"""
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', '0.0%').replace('%', '').strip()
                percent_value = int(float(percent))  # Converte "45.0%" para 45
                logging.info(f"Progresso do download: {percent_value}%")  
                socketio.emit('progress', {'progress': percent_value}, namespace="/")
            except Exception as e:
                logging.error(f"Erro ao processar progresso: {str(e)}")

    def download(self):
        """Baixa um vídeo do YouTube e emite eventos de progresso"""
        try:
            ydl_opts = {
                'format': f'bestvideo[height={self.quality}]+bestaudio/best',
                'outtmpl': os.path.join(self.output_path, 'video.%(ext)s'),
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'progress_hooks': [self.progress_hook],
                'nocheckcertificate': True,
                'no-cache-dir': True,
                'retries': 3
            }
            logging.info(f"Iniciando download: {self.url} em {self.quality}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            logging.info("Download finalizado com sucesso!")
            return os.path.join(self.output_path, 'video.mp4')

        except Exception as e:
            logging.error(f"Erro ao baixar vídeo: {str(e)}")
            return None