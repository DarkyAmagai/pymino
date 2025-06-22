from pathlib import Path
from configparser import ConfigParser
from setuptools import setup, find_packages

config = ConfigParser()
config.read('setup.cfg')

setup(
    name="pymino",
    license="MIT",
    author="DarkyAmagai",
    author_email="darkyamagai@outlook.es",
    description="Easily create a bot for Amino Apps using a modern easy to use synchronous library.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/forevercynical/pymino",
    version=config.get('metadata', 'version'),
    packages=find_packages(),
    install_requires=[
        "requests==2.32.4",
        "ujson==5.10.0",
        "colorama==0.4.6",
        "websocket-client==1.8.0",
        "diskcache==5.6.3",
        "aiohttp=3.12.13",
        "wsaccel==0.6.7",
        "dotenv==0.9.9"
    ],
    keywords=[
        "amino",
        "pymino",
        "narvii",
        "amino-api",
        "narvii-bots",
        "aminoapps",
        "amino-bot",
        "amino-bots"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8"
)
