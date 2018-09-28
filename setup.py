from setuptools import setup, find_packages


setup(
    name='threadedtweeter',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tt = threaded_tweeter.main:main',
        ],
    },
    include_package_data=True,
    data_files=[('settings.json')]
)
