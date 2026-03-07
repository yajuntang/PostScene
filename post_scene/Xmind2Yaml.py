import os
from pathlib import Path
import xmind
from ruamel.yaml import YAML


class XMindConverter:
    @staticmethod
    def is_number(s: str):
        """判定字符串是否为数字"""
        try:
            float(s.strip())
            return True
        except (ValueError, AttributeError, TypeError):
            return False

    @staticmethod
    def has_tests_title(node: dict) -> bool:
        """检查子节点是否包含 'tests' 标题"""
        return any(child.get('title') == 'tests' for child in node.get('topics', []))

    @staticmethod
    def is_end_node(node: dict) -> bool:
        """判定是否为末梢节点"""
        topics = node.get('topics', [])
        return not topics or 'topics' not in topics[0]

    def parse_node(self, node, container, is_script_mode=False):
        """递归解析 XMind 节点数据"""
        title = node.get('title', '').strip()
        topics = node.get('topics', [])

        if not is_script_mode:
            if self.has_tests_title(node):
                container[title] = {}
                for topic in topics:
                    data = {}
                    container[title][topic['title']] = data
                    self.parse_node(topic, data, True)
            else:
                container['name'] = title
                container['scene'] = []
                for topic in topics:
                    data = {}
                    container['scene'].append(data)
                    self.parse_node(topic, data, False)
        else:
            for topic in topics:
                if self.is_end_node(topic):
                    val = topic.get('topics', [{}])[0].get('title', '')
                    if self.is_number(val):
                        container[topic['title']] = float(val) if '.' in val else int(val)
                    else:
                        container[topic['title']] = val
                else:
                    data = {}
                    container[topic['title']] = data
                    self.parse_node(topic, data, True)


def xmind2Yaml(path, file_name):
    """主转换入口"""
    base_path = Path(path).resolve()
    xmind_file = base_path / f"{file_name}.xmind"
    yaml_file = base_path / f"{file_name}.yaml"

    try:
        workbook = xmind.load(str(xmind_file))
        root_data = workbook.getPrimarySheet().getRootTopic().getData()

        yaml_data = {}
        XMindConverter().parse_node(root_data, yaml_data)

        with open(yaml_file, 'w', encoding='UTF-8') as f:
            YAML().dump(yaml_data, f)
    except Exception as e:
        print(f"转换失败: {e}")