from distutils.core import setup
import os

if os.path.exists("MANIFEST"):
    os.unlink("MANIFEST")

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
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames and 'steps.py' not in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[10:]  # Strip "armstrong<dir separator>"
        for f in filenames:
            # Ignore all dot files and any compiled
            if f.startswith(".") or f.endswith(".pyc"):
                continue
            data_files.append(os.path.join(prefix, f))


[build_package(dirpath, dirnames, filenames) for dirpath, dirnames, filenames
        in os.walk('armstrong/core/arm_content')]

setup(
    name='armstrong.core.arm_content',
    version='0.2.2',
    description='A library for building news sites with multiple content types',
    author='Bay Citizen & Texas Tribune',
    author_email='dev@armstrongcms.org',
    url='http://github.com/armstrong/armstrong.core.arm_content/',
    packages=packages,
    package_data={"armstrong": data_files},
    namespace_packages=["armstrong", "armstrong.core", ],
    install_requires=[
        'Django==1.3',
        'django-model-utils==0.6.0',
        'django-reversion==1.4',
        'django-taggit==0.9.3',
        'armstrong.core.arm_sections>=0.1',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
