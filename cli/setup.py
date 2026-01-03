from setuptools import setup 

setup(
    name="hova",
    version="0.1.8",
    packages=["hova"],
    entry_point={
        "console_scripts": [
            "hova=hova.cli:main"
        ]
    }
)