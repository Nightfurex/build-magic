from setuptools import setup

from build_magic import __version__ as version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='build-magic',
    version=version,
    packages=[
        'build_magic',
    ],
    url='https://cmmorrow.github.io/build-magic/',
    license='MIT',
    author='Chris Morrow',
    author_email='cmmorrow@gmail.com',
    description='A general purpose build/install/deploy tool.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, >=3.6',
    project_urls={
        "Documentation": 'https://cmmorrow.github.io/build-magic/',
        "Source": 'https://github.com/cmmorrow/build-magic',
        "Bug Tracker": 'https://github.com/cmmorrow/build-magic/issues',
    },
    entry_points={
        'console_scripts': [
            'build-magic=build_magic.cli:build_magic',
        ],
    },
    package_data={
        'build_magic': [
            'static/*',
        ],
    },
    install_requires=[
        'click==8.0.1',
        'colorama==0.4.4',
        'cryptography==3.4.7',
        'jsonschema==4.0.1',
        'docker==5.0.2',
        'nltk==3.6.3',
        'paramiko==2.7.2',
        'python-vagrant==0.5.15',
        'PyYAML==5.4.1',
        'scp==0.14.1',
        'yaspin==2.1.0',
    ],
    tests_require=[
        'pytest',
        'freezegun',
    ],
    classifers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
)
