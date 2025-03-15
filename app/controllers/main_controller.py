import os
import logging
from flask import Blueprint, request, jsonify, send_from_directory
from app.models.downloader import YouTubeDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

main_controller = Blueprint('main_controller', __name__)

@main_controller.route('/download', methods=['POST'])
def download():
    """Rota para iniciar o download"""
    try:
        url = request.form['url']
        quality = request.form['quality']
        output_path = "downloads"  # Diretório onde os vídeos serão salvos

        if not os.path.exists(output_path):
            os.makedirs(output_path)  # Garante que a pasta existe

        logging.info(f"Recebida solicitação de download: {url} em {quality}")
        
        downloader = YouTubeDownloader(url, output_path, quality)
        file_path = downloader.download()

        if file_path:
            logging.info(f"Download concluído! Arquivo salvo em {file_path}")
            return jsonify({"success": True, "download_url": f"/download_file/{os.path.basename(file_path)}"})
        else:
            raise Exception("O download falhou")

    except Exception as e:
        logging.error(f"Erro na rota de download: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@main_controller.route('/download_file/<filename>')
def download_file(filename):
    """Baixa um arquivo salvo no servidor"""
    output_path = "downloads"
    return send_from_directory(output_path, filename, as_attachment=True)
