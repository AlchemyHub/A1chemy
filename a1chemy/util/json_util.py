import json


def write_data_to_json_file(data, path):
    json_data = json.dumps(data, ensure_ascii=False)
    fh = open(path, 'w', encoding='utf-8')
    fh.write(json_data)
    fh.close()


def read_json_from_file(path):
    fd = open(path)
    li = fd.readlines()
    return json.loads(''.join(li))
