from setuptools import setup, find_packages

setup(
    name="my_env",
    version="1.0",
    author="yuanming",
    author_email="ironGYI@163.com",
    description="use for me",

    entry_points={
        'console_scripts': ['me = my_env.cmd:Main']
        },
    packages=find_packages()
)