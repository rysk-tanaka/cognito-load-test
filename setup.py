from setuptools import find_packages, setup

setup(
    name="cognito-load-test",
    packages=find_packages(
        include=[
            "cognito_load_test",
            "cognito_load_test.*",
        ]
    ),
)
