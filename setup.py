from setuptools import setup

setup(
    name='pylacuna',
    version='0.0.1',
    description='Calculates a study path for students.',
    url='https://github.com/miketwo/pylacuna',
    keywords="pylacuna students",
    packages=['pylacuna'],
    scripts=[
        'bin/pylacuna',
        'bin/pylacuna_run_tests.sh'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    long_description=open('README.md', 'r').read(),
    install_requires=[
        # Main
        'requests', 'requests[security]', 'python-dateutil',
        # Caching
        'redis', 'redis-simple-cache',
        # Dev/Test packages
        'ipdb', 'ipython', 'mock', 'nose', 'pep8', 'pyflakes',
        # Docs packages
        'recommonmark'],
    )
