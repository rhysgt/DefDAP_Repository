from setuptools import setup, find_packages

setup(
    name='DefDAP_Repository',
    author='Rhys Thomas',
    author_email='rhys.thomas@manchester.ac.uk',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.8',
    install_requires=[
        'pooch',
        'defdap',
        'numpy',
        'yaml',
        'glob',
        'matplotlib>=3.0.0'
    ],
)
