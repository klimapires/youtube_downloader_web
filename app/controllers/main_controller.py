import os
import logging
from flask import Blueprint, render_template, request, jsonify, send_from_directory
from app.models.downloader import YouTubeDownloader
from app.utils.file_utils import save_last_directory, load_last_directory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

main_controller = Blueprint('main_controller', __name__)

@main_controller.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_controller.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        quality = request.form['quality']
        output_path = load_last_directory()

        logging.info(f"Iniciando download de {url} com qualidade {quality}")

        downloader = YouTubeDownloader(url, output_path, quality)
        file_path = downloader.download()

        logging.info(f"Download concluído: {file_path}")

        return jsonify({"success": True, "download_url": f"/download_file/{os.path.basename(file_path)}"})
    except Exception as e:
        logging.error(f"Erro no download: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@main_controller.route('/download_file/<filename>')
def download_file(filename):
    output_path = load_last_directory()
    return send_from_directory(output_path, filename, as_attachment=True)
