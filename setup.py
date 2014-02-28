from setuptools import setup, find_packages

version = "0.1"

setup(name='sims',
      version=version,
      description='Data exporter in xml format for simshab project',
      url='www.eaudeweb.ro',
      author='Ovidiu Miron',
      author_email='ovidiu.miron@eaudeweb.ro',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False)
