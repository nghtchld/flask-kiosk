from setuptools import setup

setup(
    name='restaurant-kiosk',
    packages=['kiosk'],
    include_package_data=True,
    install_requires=[
        'flask','flask-wtf','python-dotenv','duckdb'
    ],
)