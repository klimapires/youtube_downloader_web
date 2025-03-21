import os
import logging
from flask import Blueprint, request, jsonify, send_file
from app.models.downloader import YouTubeDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

main_controller = Blueprint('main_controller', __name__)

@main_controller.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get('url')
        quality = request.form.get('quality')

        if not url or not quality:
            logging.error("Erro: URL ou qualidade não fornecidos.")
            return jsonify({"success": False, "error": "URL ou qualidade ausentes."}), 400

        logging.info(f"Iniciando download de {url} com qualidade {quality}")

        # Criar um diretório temporário para armazenar o arquivo antes do envio
        temp_dir = "/tmp/youtube_downloads"
        os.makedirs(temp_dir, exist_ok=True)

        downloader = YouTubeDownloader(url, temp_dir, quality)
        file_path = downloader.download()

        if not file_path or not os.path.exists(file_path):
            logging.error("Erro: O arquivo de saída não foi gerado corretamente.")
            return jsonify({"success": False, "error": "Falha ao gerar o arquivo de saída."}), 500

        logging.info(f"Download concluído: {file_path}")

        # Enviar o arquivo diretamente para o usuário e deletar depois do envio
        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)  # Remover o arquivo temporário após envio
        return response

    except Exception as e:
        logging.error(f"Erro no download: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
