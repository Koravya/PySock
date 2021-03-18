
from setuptools import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name="pysock",
    install_requires=install_requires,
    version="0.1",
    description="Socket Implementation of Sockets for object messaging",
    py_modules = ["PySock\\PySock"]
)
