from setuptools import setup, find_packages

setup(
    name = 'mypy-zope',
    version = '0.1',
    author = 'Andrey Lebedev',
    author_email = 'andrey.lebedev@gmail.com',
    description = 'Plugin for mypy to support zope interfaces',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires = [
        'mypy',
        'zope-interface',
        'zope-schema'
    ],
    extras_require={'test': ["pytest>=4.0.0,<4.1.0", "pytest-cov"]},

)
