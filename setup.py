"""
Setup for indico apis
"""

from setuptools import setup, find_packages

setup(
    name="intercombot",
    version="0.1.0",
    packages=find_packages(),
    description="""
        Automatic message triage with the indico custom collections API
    """,
    license="MIT License (See LICENSE)",
    url="https://github.com/IndicoDataSolutions/intercombot",
    install_requires=[
        'python-intercom >= 2.1.1',
        'tornado == 4.4.1',
        'html2text == 2016.9.19',
        'indicoio == 0.16.3'
    ]
)
