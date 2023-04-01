from setuptools import find_packages, setup

setup(
    name='digimind',
    packages=find_packages(),
    version= '0.0.4',
    description= 'DigiMind - Remaining Cycle Time Predictor',
    author='DigiMind Team',
    long_description = open("README.md").read(),
    license='MIT'
)