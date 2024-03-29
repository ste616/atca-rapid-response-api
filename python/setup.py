from setuptools import setup

# This is the atca_rapid_response_api Python library.
# Jamie Stevens 2017
# ATCA Senior Systems Scientist
# Jamie.Stevens@csiro.au

setup(name='atca_rapid_response_api',
      version='1.3',
      description='ATCA Rapid Response Mode API',
      url='https://github.com/ste616/atca-rapid-response-api',
      author='Jamie Stevens',
      author_email='Jamie.Stevens@csiro.au',
      license='MIT',
      packages=[ 'atca_rapid_response_api' ],
      install_requires=[
          'requests'
      ],
      zip_safe=False)

# Changelog:
# 2017-04-04, v1.1: Prevented some SSL checks, because namoi's SSL is still a little
#   flaky.
# 2017-04-10, v1.2: Added the maximumLag option.
# 2023-10-09, v1.3: Can now use HTTP authentication to the service
