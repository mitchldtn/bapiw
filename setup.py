from setuptools import setup, find_packages

setup(
    name='bapiw',

    version='0.0.1',

    description='Binance API Wrapper',
    long_description='Package used to pull and parse data from the Binance API',

    url='https://github.com/mitchldtn/bapiw',

    author='mitchldtn',
    author_email='mitchldtn@protonmail.com',

    packages=['bapiw'],
    install_requires=['requests', 'pandas', 'numpy']
)