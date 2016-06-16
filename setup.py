
from setuptools import setup

setup(name='thermalmodel',
      version='0.1',
      description="A thermal model of the tower a the scdms Queen's test facility",
      author='Caleb Jonker',
      author_email='caleb.jonker@queensu.ca',
      license='MIT',
      packages=['thermalmodel'],
      package_data={'mypkg': ['data/*.csv']},
      zip_safe=False)
