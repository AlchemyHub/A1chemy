import setuptools

with open('./README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="a1chemy",
    version="0.0.2",
    author="zh",
    author_email="z@a1chemy.com",
    description="alchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ged0/V",
    packages=setuptools.find_packages(exclude=['tests', 'notebook']),  # 安装的时候过滤掉tests和notebook文件夹
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
