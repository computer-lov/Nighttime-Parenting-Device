from setuptools import setup

setup(name='nighttimeParenting', 
      version='1.0',
      description='Infrastructure Layer for Project',
      author=['Andrew Paul Mayer', 'Aron Goldberg', 'Beatriz Perez'],
      author_email='apm532@nyu.edu',
      url='git@github.com:computer-lov/Nighttime-Parenting-Device.git',
      install_requires=['spidev','pygame','adafruit-circuitpython-ssd1327','adafruit-circuitpython-display-text'],
      py_modules=['nighttimeParenting']
      )
