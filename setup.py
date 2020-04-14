from setuptools import setup, find_packages

setup(
    name='parking_lot',
    url='',
    author='Rory Houlihan',
    version=1.0,
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'unit_tests']),
    install_requires=['flask',
                      'requests'],
    setup_requires=['wheel'],
    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ]
    }
)
