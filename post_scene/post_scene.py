import json
import os

import requests
from ruamel.yaml import YAML

from post_scene.Xmind2Yaml import xmind2Yaml
from post_scene.creator import PostmanJson
from post_scene.parser import Utils, Parse

class PostScene:
    @staticmethod
    def check_postman_url(url: str):
        if url.startswith('http'):
            data = requests.get(url, timeout=60).json()
        else:
            data = json.load(open(url, encoding='utf-8'))
        return data

    @staticmethod
    def package(scenes_val, postman_data):
        new_items = []
        for scene in scenes_val:
            if 'scene' in scene:
                folder = {
                    'name': scene['name'],
                    'item': PostScene.package(scene['scene'], postman_data)
                }
                if len(scene['auth']) > 0:
                    folder['auth'] = scene['auth']
                new_items.append(folder)
            else:
                postman_item = Utils.find_postman_item_by_name(scene['name'], postman_data['item'])
                if postman_item is not None:
                    postman_item['request'] = Utils.replace_params_name(postman_item['request'], scene['params-name'])
                    Utils.replace_auth_data(postman_item['request'],scene['auth'])
                    postman_item['event'] = []
                    if 'pre-scripts' in scene:
                        postman_item['event'].append(PostmanJson.create_script(scene['pre-scripts']))
                    if 'scripts' in scene:
                        postman_item['event'].append(PostmanJson.create_script(scene['scripts'], 'test'))
                        new_items.append(postman_item)
        return new_items

    @staticmethod
    def generate(yaml_path, postman_data_path, scene_dirs='../scene'):
        file = open(yaml_path, 'r', encoding='utf-8')
        yaml = YAML()
        script = yaml.load(file)

        scenes = Parse.parse_scene(script['scene'])

        postman_data = PostScene.check_postman_url(postman_data_path)
        postman_items = []
        new_postman_data = {"info": PostmanJson.create_info(script['name']), 'item': postman_items}

        if 'auth' in script:
            new_postman_data['auth'] = {}
            Parse.parse_auth(script,new_postman_data['auth'])

        if 'variable' in postman_data:
            new_postman_data['variable'] = postman_data['variable']

        postman_items.extend(PostScene.package(scenes, postman_data))

        os.makedirs(scene_dirs, exist_ok=True)
        file = open(os.path.join(scene_dirs, '{0}.json'.format(script['name'])), 'w+')
        file.write(json.dumps(new_postman_data, indent=4))


    @staticmethod
    def covert(script_path, postman_data_path, scene_dirs='./scene'):
        if script_path.endswith('.yaml'):
            PostScene.generate(script_path, postman_data_path, scene_dirs)
        elif script_path.endswith('.xmind'):
            os.path.dirname(script_path)
            xmind2Yaml(os.path.dirname(script_path), os.path.basename(script_path).replace('.xmind', ''))
            PostScene.generate(script_path.replace('.xmind', '.yaml'), postman_data_path, scene_dirs)
