from setuptools import setup, find_packages


setup(
    name='threadedtweeter',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tt = threaded_tweeter.parser:main',
        ],
    }
)
