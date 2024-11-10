from setuptools import find_packages, setup

setup(
    name="cognito-load-test",
    packages=find_packages(
        include=[
            "src",
            "src.*",
        ]
    ),
)
