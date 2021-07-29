from setuptools import find_packages
from distutils.core import setup
import os
import io


def readfile(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    contents = io.open(path, encoding='utf8').read()
    return contents


setup(
    name="bcdpy",
    version='0.1',
    description='Python wrapper for the Better Call Dev API',
    long_description=readfile('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests'],
    author=u'Doug Fenstermacher',
    author_email='douglas.fenstermacher@gmail.com',
    url='https://github.com/dpfens/bcdpy',
    keywords='tezos, blockchain, contract, block, account, token',
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ]
)
