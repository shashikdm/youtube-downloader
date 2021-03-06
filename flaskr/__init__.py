import os

from flask import Flask

from . import youtube_downloader

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(youtube_downloader.bp)

    youtube_downloader.pytube_cache.init_app(app)

    # a simple page that says hello
    @app.route('/status')
    def status():
        return 'OK'

    return app
