from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="pymino",
    license="MIT",
    author="forevercynical",
    version="1.1.1.3",
    author_email="me@cynical.gg",
    description="Amino API wrapper to make bots easier to use",
    url="https://github.com/forevercynical/pymino",
    packages=find_packages(),
    long_description = (Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=[
    "requests",
    "colorama==0.4.6",
    "websocket-client==1.4.1",
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
    python_requires=">=3.7"
)
