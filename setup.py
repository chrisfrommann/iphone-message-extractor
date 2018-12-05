from setuptools import setup

setup(name='iphone_message_extractor',
      version='0.1.0',
      description='Simple CLI to extract messages (SMS/iMessage) to CSV from iPhone backups',
      url='https://github.com/chrisfrommann/iphone-message-extractor',
      author='Chris Frommann',
      author_email='c2+gh@cwf.nyc',
      license='LGPLv3',
      packages=['iphone_message_extractor'],
      install_requires=[
          'phonenumbers',
      ],
      zip_safe=False)