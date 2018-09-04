from setuptools import setup

setup(
    name='threadedtweeter',
    entry_points={
        'console_scripts': [
            'tt = threaded_tweeter.base_parser:main',
        ],
    }
)