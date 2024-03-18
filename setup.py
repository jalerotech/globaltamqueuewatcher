from setuptools import setup, find_packages

setup(name='GlobalTAMQueueWatcher',
      author='Joshua Alero',
      version='1.0',
      description='GlobalTAMQueueWatcher',
      packages=find_packages(),
      install_requires=['python-dotenv',
                        'requests',
                        'pathlib',
                        'dotenv',
                        'datetime'
                        ]
      )