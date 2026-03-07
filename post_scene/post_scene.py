import json
import logging
from pathlib import Path
import requests
from ruamel.yaml import YAML
from post_scene.Xmind2Yaml import xmind2Yaml
from post_scene.creator import PostmanJson
from post_scene.parser import Utils, Parse

class PostScene:
    @staticmethod
    def fetch_postman_data(source: str):
        """获取远程或本地 Postman 数据"""
        try:
            if source.startswith('http'):
                resp = requests.get(source, timeout=30)
                resp.raise_for_status()
                return resp.json()
            with open(source, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Postman 数据加载异常: {e}")
            return None

    @staticmethod
    def package(scenes_val, postman_data):
        """构建 Postman Collection 层级结构"""
        new_items = []
        for scene in scenes_val:
            if 'scene' in scene:
                folder = {
                    'name': scene['name'],
                    'item': PostScene.package(scene['scene'], postman_data)
                }
                if scene.get('auth'):
                    folder['auth'] = scene['auth']
                new_items.append(folder)
            else:
                item = Utils.find_postman_item_by_name(scene['name'], postman_data['item'])
                if item:
                    # 使用深拷贝确保数据独立性
                    target = json.loads(json.dumps(item))
                    target['request'] = Utils.replace_params_name(target['request'], scene['params-name'])
                    Utils.replace_auth_data(target['request'], scene['auth'])
                    target['event'] = []
                    if 'pre-scripts' in scene:
                        target['event'].append(PostmanJson.create_script(scene['pre-scripts']))
                    if 'scripts' in scene:
                        target['event'].append(PostmanJson.create_script(scene['scripts'], 'test'))
                    new_items.append(target)
        return new_items

    @staticmethod
    def generate(yaml_path, postman_data_path, scene_dirs='../scene'):
        """生成 Postman 脚本文件"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            script = YAML().load(f)

        scenes = Parse.parse_scene(script['scene'])
        postman_data = PostScene.fetch_postman_data(postman_data_path)
        if not postman_data: return

        new_collection = {
            "info": PostmanJson.create_info(script['name']),
            "item": PostScene.package(scenes, postman_data)
        }

        if 'auth' in script:
            new_collection['auth'] = {}
            Parse.parse_auth(script, new_collection['auth'])
        if 'variable' in postman_data:
            new_collection['variable'] = postman_data['variable']

        output_path = Path(scene_dirs) / f"{script['name']}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(new_collection, f, indent=4, ensure_ascii=False)