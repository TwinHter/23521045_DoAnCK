import itertools
import string
import time
from zipfile import ZipFile
import json

data = {}
def get_data(state, title, content, timee):
    # Trả về dữ liệu JSON
    if state:
        data_to_share = {
            'title': title,
            'content': content,
            'timee': timee
        }
    else:
        data_to_share = {
            'title': 'Failed to Cracking',
            'content': '',
            'timee': ''
        }
    return data_to_share

def start_cracking():
    global data
    str_zipFile = 'example.zip'
    chars = string.digits  # Sử dụng tất cả các số từ 0 đến 9
    max_length = 6
    start_time = time.time()

    is_find = False
    for length in range(1, max_length + 1):
        if is_find == True:
            break
        for combination in itertools.product(chars, repeat=length):
            if is_find == True:
                break
            str_pwd = "".join(combination)

            try:
                with ZipFile(str_zipFile) as zipObj:
                    zipObj.extractall(pwd=bytes(str_pwd, 'utf-8'))
                    end_time = time.time()
                    time_taken = int((end_time - start_time) * 1000)
                    data = get_data(1, "Cracking Successfully", f"Password found: {str_pwd}", f"Time taken: {time_taken} miliseconds")
                    is_find = True
            except RuntimeError as e:
                continue

    if not is_find:
        data = get_data(0, '', '', '')

start_cracking()
with open('data.json', 'w') as json_file:
    json.dump(data, json_file)
