from setuptools import setup, find_packages

setup(name='kai',
      version='0.0.1',
      description='Konveyor AI source code modernization',
      url='https://github.com/konveyor-ecosystem/kai',
      author='Konveyor Community',
      author_email='konveyor-dev@googlegroups.com',
      license='Apache Software License 2.0',
      packages=find_packages(where='src'),
      zip_safe=False)
