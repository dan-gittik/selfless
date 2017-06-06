import setuptools


package = dict(
    name             = 'selfless',
    version          = '0.1.0',
    author           = 'Dan Gittik',
    author_email     = 'dan.gittik@gmail.com',
    description      = 'A nifty decorator to get rid of the unnecessary self parameter in methods.',
    license          = 'MIT',
    url              = 'https://github.com/dan-gittik/selfless',
    packages         = setuptools.find_packages(),
    install_requires = [
    ],
    tests_require    = [
        'pytest',
    ],
)


if __name__ == '__main__':
	setuptools.setup(**package)
