from setuptools import setup 

setup(
    name="hova",
    version="1.95",
    packages=["hova"],
    entry_point={
        "console_scripts": [
            "hova=hova.cli:main"
        ]
    }
)