from setuptools import setup, find_packages

setup(name='tambacklogbuddy',
      author='Joshua Alero',
      version='1.0',
      url='https://gitlab-sjc.cisco.com/jalero/tambacklogbuddy.git',
      description='tambacklogbuddy',
      packages=find_packages('.'),
      install_requires=['python-dotenv',
                        'requests',
                        'pathlib',
                        'dotenv',
                        'datetime'
                        ]
      )
