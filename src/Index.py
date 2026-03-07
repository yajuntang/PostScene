from pathlib import Path
from post_scene.post_scene import PostScene

# 动态获取项目根目录
CURRENT_DIR = Path(__file__).resolve().parent
YAML_PATH = CURRENT_DIR / 'yaml' / 'demo.yaml'
XMIND_PATH = CURRENT_DIR / 'xmind' / 'demo.xmind'
API_DOC_PATH = CURRENT_DIR / 'api_document' / 'demo.postman_collection.json'


def main():
    print("PostScene 启动转换流程...")

    # 自动转换并生成场景
    PostScene.covert(
        script_path=str(YAML_PATH),
        postman_data_path=str(API_DOC_PATH),
        scene_dirs=str(CURRENT_DIR / 'scene')
    )

    print(f"✅ 生成完毕，结果已保存至: {CURRENT_DIR / 'scene'}")


if __name__ == "__main__":
    main()