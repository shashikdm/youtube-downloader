def test_index(client):
    response = client.get('/')

    assert b'Youtube Downloader' in response.data
    assert b'Video Link' in response.data

def test_details(client):
    response = client.get('/details?url=https://youtube.com/watch?v=XJGiS83eQLk')

    assert b'Resolutions' in response.data
    assert b'Audio' in response.data
    assert b'Subtitles' in response.data

def test_request_download(client):
    response = client.post('/request_download', json={'videoId': 'XJGiS83eQLk', 'iTag': 249}, content_type='application/json')

    assert b'download' in response.data

def test_download(client):
    file_hash = 'en (en).srt'
    response = client.get('/download?fileHash={}'.format(file_hash))

    assert b'subtitles' in response.data
