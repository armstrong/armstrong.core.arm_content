from setuptools import setup

setup(
    name='armstrong.core.arm_content',
    version='0.1',
    description='A library for building news sites with multiple content types',
    author='Texas Tribune',
    author_email='tech@texastribune.org',
    url='http://github.com/texastribune/armstrong.core.arm_content/',
    # TODO: generate this dynamically
    packages=[
        'armstrong',
        'armstrong.core',
        'armstrong.core.arm_content',
        'armstrong.core.arm_content.tests',
        'armstrong.core.arm_content.tests.fields',
        'armstrong.core.arm_content.tests.models',
        'armstrong.core.arm_content.video',
        'armstrong.core.arm_content.video.backends',
    ],

    install_requires=[
        'distribute',
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
