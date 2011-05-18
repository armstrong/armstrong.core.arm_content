from distutils.core import setup
import os

# Borrowed and modified from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

def build_package(dirpath, dirnames, filenames):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    pkg = dirpath.replace(os.path.sep, '.')
    if os.path.altsep:
        pkg = pkg.replace(os.path.altsep, '.')
    packages.append(pkg)

[build_package(dirpath, dirnames, filenames) for dirpath, dirnames, filenames in os.walk('armstrong')]

setup(
    name='armstrong.core.arm_content',
    version='0.1',
    description='A library for building news sites with multiple content types',
    author='Bay Citizen & Texas Tribune',
    author_email='dev@texastribune.org',
    url='http://github.com/armstrong/armstrong.core.arm_content/',
    packages=packages,
    install_requires=[
        'Django==1.3',
        'django-model-utils==0.6.0',
        'django-reversion==1.4',
        'django-taggit==0.9.3',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
