from setuptools import setup, find_packages

setup(
    name='bao',
    version='0.1.0',
    description='用户注册登录系统包',
    author='Your Name',
    author_email='your_email@example.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bao = bao.main:main',
        ],
    },
)