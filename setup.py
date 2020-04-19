from os import path as os_path
from setuptools import setup


this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='PostScene',  # 包名
    python_requires='>=3.7.0', # python环境
    version="1.0.0", # 包的版本
    description="一个强大的工具，基于 Postman 接口自动化场景设计",  # 包简介，显示在PyPI上
    long_description=read_file('README.md'), # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="cheryl tong", # 作者相关信息
    author_email='cheryl_98750@163.com',
    url='https://gitee.com/tangyajun/PostScene',
    install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    include_package_data=True,
    license="GNU Affero General Public License v3 ",
    keywords=['scene','postman','automation','testing','api'],
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Affero General Public License v3 ',
        'Programming Language :: Python :: 3.7',
    ],
)