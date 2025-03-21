import os
import logging
from app import socketio
from yt_dlp import YoutubeDL

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
        if not self.output_path:
            logging.error("Erro: O diretório de saída está indefinido.")
            return None

        os.makedirs(self.output_path, exist_ok=True)

        # Configurar User-Agent para se parecer com um navegador
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        ydl_opts = {
            'format': f'bestvideo[height={self.quality}]+bestaudio/best',
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'no-check-certificate': True,
            'sleep-requests': 1,
            'retries': 5,
            'fragment-retries': 5,
            'extractor-args': {
                'youtube': {
                    'player-client': ['android', 'tvhtml5', 'ios']  # Simula diferentes clientes
                }
            },
            'http_headers': {
                'User-Agent': "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
            }
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(self.url, download=True)
                file_path = ydl.prepare_filename(info)

                if not file_path or not os.path.exists(file_path):
                    logging.error("Erro: O arquivo não foi baixado corretamente.")
                    return None

                return file_path

            except Exception as e:
                logging.error(f"Erro ao baixar o vídeo: {e}")
                return None