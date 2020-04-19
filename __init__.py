import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PostScene",
    version="1.0.0",
    author="cheryl Tong",
    author_email="cheryl_98750@163.com",
    description="一个强大的工具，基于 Postman 接口自动化场景设计",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/tangyajun/PostScene.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
)