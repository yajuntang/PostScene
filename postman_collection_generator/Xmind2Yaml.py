import os

import xmind
from ruamel.yaml import YAML


def is_number(s: str):
    s = s.strip()
    if s.isdigit():
        return True
    if s.count('.') == 1:
        left = s.split('.')[0]
        right = s.split('.')[1]
        if right.isdigit():
            if left.count('-') == 1 and left.startswith('-'):
                num = left[1:]
                if num.isdigit():
                    return True
            elif left.isdigit():
                return True
    elif s.startswith('-') and s.count('-') == 1:
        return s[1:].isdigit()

    return False


def has_tests_title(node: dict) -> bool:
    if 'topics' in node:
        for child in node['topics']:
            if child['title'] == 'tests':
                return True
    return False


def is_end(node: dict) -> bool:
    topics = node['topics']
    return 'topics' not in topics[0]


def parse_xmind_data(xmind_node, yaml_data, is_script):
    if not is_script:
        if has_tests_title(xmind_node):  # 判断子节点是否有tests
            yaml_data[xmind_node['title']] = {}
            if 'topics' in xmind_node:
                topics = xmind_node['topics']
                for topic in topics:
                    data = {}
                    yaml_data[xmind_node['title']][topic['title']] = data
                    parse_xmind_data(topic, data, True)
        else:
            yaml_data['name'] = xmind_node['title']
            yaml_data['scene'] = []
            if 'topics' in xmind_node:
                topics = xmind_node['topics']
                for topic in topics:
                    data = {}
                    yaml_data['scene'].append(data)
                    parse_xmind_data(topic, data, False)
    else:
        if 'topics' in xmind_node:
            topics = xmind_node['topics']
            for topic in topics:

                if is_end(topic):
                    data = topic['topics'][0]['title']
                    if is_number(data): data = int(data)
                    yaml_data[topic['title']] = data
                else:
                    data = {}
                    yaml_data[topic['title']] = data
                    parse_xmind_data(topic, data, True)


def xmind2Yaml(path, file_name):
    file_path = os.path.join(os.path.abspath(path), file_name + ".xmind")
    workbook = xmind.load(file_path)
    xmind_data = workbook.getPrimarySheet().getRootTopic().getData()
    yaml_data = {}
    parse_xmind_data(xmind_data, yaml_data, False)
    stream = open(os.path.join(os.path.abspath(path), file_name + ".yaml"), 'w', encoding='UTF-8')
    yaml = YAML()
    yaml.dump(yaml_data, stream)

xmind2Yaml('../', '自动化测试')


