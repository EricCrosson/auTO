from setuptools import setup

setup(name='autoto',
      version='0.0.1',
      description='Automatic tournament orgamizer',
      url='http://github.com/EricCrosson/auTO',
      author='Eric Crosson, Dave Cusatis',
      author_email='eric.s.crosson@utexas.edu, davecusatis1@gmail.com',
      license='AGPLv3',
      packages=['autoto'],
      install_requires=[
          'Flask',
      ],
      dependency_links=['http://github.com/russ-/pychallonge#egg=pychallonge'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
