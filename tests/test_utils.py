import pytest
from flaskr.utils import *

def test_get_download_link():
    result = get_download_link('/dummy_path')

    assert result == '/download?fileHash=dummy_path'

def test_hash_encrypt():
    result = hash_encrypt('dummy_file_name')

    assert result == 'dummy_file_name'

def test_hash_decrypt():
    result = hash_decrypt('dummy_file_name')

    assert result == 'dummy_file_name'
