from setuptools import setup

setup(
    name='threadedtweeter',
    entry_points={
        'console_scripts': [
            'tt = parser.base_parser:main',
        ],
    }
)