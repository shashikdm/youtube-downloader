from flask import (
    Blueprint, flash, render_template, request, send_from_directory
)
from werkzeug.exceptions import abort
from pytube import YouTube, extract
from os import path
from uuid import uuid4

from .utils import *
from .constants import *

from flask_caching import Cache

pytube_cache = Cache(config={
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
})

bp = Blueprint('youtube_downloader', __name__)

@bp.route('/')
def index():
    return render_template('youtube_downloader/index.html')

@bp.route('/details')
def details():
    url = request.args['url']
    error = None

    if not url:
        error = 'Video link is required.'

    if error is not None:
        flash(error)
    else:
        video_id = extract.video_id(url)
        video = pytube_cache.get(video_id)

        if video is None:
            video = YouTube(url)
            pytube_cache.set(video_id, video)

        return render_template('youtube_downloader/details.html', video=video)

@bp.route('/request_download', methods=['POST'])
def request_download():
    data = request.get_json()

    error = None
    if 'videoId' not in data:
        error = 'videoId is required'
    elif 'isCaption' in data and 'captionCode' not in data:
        error = 'captionCode is required'
    elif 'isCaption' not in data and 'iTag' not in data:
        error = 'iTag is required'
    if error is not None:
        return error, 400

    video_id = data['videoId']
    is_caption = 'isCaption' in data

    video = pytube_cache.get(video_id)
    if video is None:
        video_url = 'www.youtube.com?v=' + video_id
        video = YouTube(video_url)
        pytube_cache.set(video_id, video)

    file_path = youtube_download(video, is_caption, data)
    return get_download_link(file_path)

def youtube_download(video, is_caption, data):
    print('still downloading')
    uuid = str(uuid4())
    if is_caption:
        caption_code = data['captionCode']
        file_path = video.captions[caption_code].download(caption_code, output_path=DOWNLOADS_DIR, filename_prefix=uuid)
    else:
        i_tag = data['iTag']
        file_path = video.streams.get_by_itag(i_tag).download(DOWNLOADS_DIR, filename_prefix=uuid)
    return file_path

@bp.route('/download')
def download():
    file_hash = request.args['fileHash']

    if not file_hash:
        return 'file_hash is required', 400

    file_name = hash_decrypt(file_hash)

    file_path = DOWNLOADS_DIR + file_name

    if not path.isfile(file_path):
        return 'file not found', 404

    return send_from_directory(directory = FLASK_DOWNLOAD_DIR, filename= file_name, as_attachment=True, attachment_filename=strip_uuid(file_name))
