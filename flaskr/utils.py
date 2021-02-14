def get_download_link(file_path):
    return '/download?fileHash={}'.format(hash_encrypt(file_path.split('/')[-1]))

def hash_encrypt(file_name):
    return file_name

def hash_decrypt(file_hash):
    return file_hash

def strip_uuid(file_name):
    return file_name[36:]