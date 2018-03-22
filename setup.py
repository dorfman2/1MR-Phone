# Setup script for 1MR-Phone
# Version 2.0
try:
    from setuptools import setup
    test_extras = {}
except ImportError:
    from distutils.core import setup
    test_extras = {}
    
setup(
      name='1MR-Phone',
      version='2.0.0',
      description='MP3 Rotary Telephone',
      long_description=open('README.txt').read(),
      url='https://github.com/dorfman2/1MR-Phone.git',
      platforms='any',
      author='dorfman2',
      author_email='dorfman2@buffalo.edu',
      license='MIT',
      packages=['1MR-Phone'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: System :: Networking',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3'],
      install_requires=[
          'python-osc'],
      scripts = [
        'bin/install-script.sh'
      ],
      zip_safe=False)
