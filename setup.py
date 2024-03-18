from setuptools import setup, find_packages

setup(name='GlobalTAMQueueWatcher',
      author='Joshua Alero',
      version='1.0',
      url='https://gitlab-sjc.cisco.com/jalero/globaltamqueuewatcher.git',
      description='GlobalTAMQueueWatcher',
      packages=find_packages(),
      install_requires=['python-dotenv',
                        'requests',
                        'pathlib',
                        'datetime'
                        ]
      )