from flask import Blueprint, render_template, request, send_from_directory, jsonify, redirect, url_for
import os
from app.models.downloader import YouTubeDownloader
from app.utils.file_utils import save_last_directory, load_last_directory

main_controller = Blueprint('main_controller', __name__)

@main_controller.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        quality = request.form['quality']
        output_path = load_last_directory()

        if not url or not quality:
            return render_template('index.html', error="Por favor, preencha todos os campos.")

        try:
            downloader = YouTubeDownloader(url, output_path, quality)
            file_path = downloader.download()
            return send_from_directory(output_path, 'temp_video.mp4', as_attachment=True)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

@main_controller.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        quality = request.form['quality']
        output_path = load_last_directory()

        downloader = YouTubeDownloader(url, output_path, quality)
        file_path = downloader.download()

        return jsonify({
            "success": True,
            "download_url": f"/download_file/{os.path.basename(file_path)}"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main_controller.route('/download_file/<filename>')
def download_file(filename):
    output_path = load_last_directory()
    return send_from_directory(output_path, filename, as_attachment=True)

@main_controller.route('/set_directory', methods=['POST'])
def set_directory():
    output_path = request.form['output_path']
    save_last_directory(output_path)
    return redirect(url_for('main_controller.index'))