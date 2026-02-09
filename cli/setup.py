from setuptools import setup 

setup(
    name="hova",
    version="2.0",
    packages=["hova"],
    entry_point={
        "console_scripts": [
            "hova=hova.cli:main"
        ]
    }
)