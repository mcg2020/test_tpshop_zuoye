import os
import json


def read_data():
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/data/data.json"
    with open(file_path, mode='r', encoding='utf-8') as f:
        jsonData = json.load(f)
        result_list = []
        for data in jsonData:
            username = data.get("username")
            reg_password = data.get("reg_password")
            login_password = data.get("login_password")
            status = data.get("status")
            reg_msg = data.get("reg_msg")
            login_msg = data.get("login_msg")
            http_code = data.get("http_code")
            result_list.append((username, reg_password, login_password, status, reg_msg, login_msg, http_code))
            print(result_list)
            return result_list