from setuptools import setup

setup(
    name='Home Server',
    packages=['HomeServer'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
