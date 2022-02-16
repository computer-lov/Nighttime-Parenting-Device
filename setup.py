from setuptools import setup

setup(name='micCircuit', 
      version='1.0',
      description='Library for baby monitoring subsystem',
      author='Andrew Paul Mayer',
      author_email='apm532@nyu.edu',
      url='git@github.com:computer-lov/Nighttime-Parenting-Device.git',
      install_requires=['RPi.GPIO'],
      py_modules=['micCircuit']
      )