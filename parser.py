import json
from datetime import datetime
import os
import base64

def mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def mkuser(username):
    mkdir(f"{username}")
    mkdir(f"{username}/blog")
    mkdir(f"{username}/story")
    mkdir(f"{username}/page")

def process(data):
    body = data['body']['und'][0]
    node_id = data['nid']
    created = datetime.fromtimestamp(int(data['created']))
    changed = datetime.fromtimestamp(int(data['changed']))

    meta_data = {
        'format': body['format'],
        'title': data["title"],
        'changed': changed.strftime("%Y-%m-%d %H:%M:%S"),
        'created': created.strftime("%Y-%m-%d %H:%M:%S"),
        'nid': node_id,
    }
    if data['path'] != False:
        meta_data['alias'] = data['path']['alias']
    for key in data.keys():
        if key.startswith('taxonomy_vocabulary'):
            taxonomy_vocabulary = data[key]
            if len(taxonomy_vocabulary) > 0:
                tids = list(map(lambda foo:foo['tid'], taxonomy_vocabulary['und']))
                meta_data['taxonomy'] = tids

    created_str = created.strftime("%Y-%m-%d %H-%M")
    title = data["title"].replace('/', '／') # 全角替换
    path = f'{data["name"]}/{data["type"]}/{created_str}-{title}'
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    txt_filename = f'{path}/{node_id}.txt'
    html_filename = f'{path}/{node_id}.html'
    meta_filename = f'{path}/meta.json'
    with open(txt_filename, "w", encoding='utf8') as txt:
        txt.write(body['value'])
    with open(html_filename, "w", encoding='utf8') as html:
        html.write(body['safe_value'])
    with open(meta_filename, "w", encoding='utf8') as meta:
        json.dump(meta_data, meta, ensure_ascii=False)
    if 'upload' in data and len(data['upload']) > 0:
        uploads = data['upload']['und']
        for upload in uploads:
            blob = base64.b64decode(upload['node_export_file_data'])
            with open(f'{path}/{upload["filename"]}', "wb") as f:
                f.write(blob)

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as file:
        mkuser('admin')
        for data in json.load(file):
            if data['name'] == 'admin':
                process(data)
