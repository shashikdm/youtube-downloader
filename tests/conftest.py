import os
import flask
import tempfile

import pytest
from flaskr import create_app

@pytest.fixture
def app(mocker):

    app = create_app({
        'TESTING': True,
    })

    mocker.patch('flaskr.youtube_downloader.youtube_download', return_value='dummy_file_name')
    mocker.patch('os.path.isfile', return_value=True)
    mocker.patch('flaskr.youtube_downloader.send_from_directory', return_value='subtitles')

    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()