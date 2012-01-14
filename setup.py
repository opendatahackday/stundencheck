from setuptools import setup, find_packages

setup(
    name = 'stundencheck',
    version = '0.3a',
    packages = find_packages(),
    install_requires = [
        'python-dateutil>=1.2',
        'SQLAlchemy==0.7.3',
        'Flask==0.8',
        ],
    setup_requires=[
        'nose==1.1.2'
        ],
    # metadata for upload to PyPI
    author = 'Open Data Hack Day',
    author_email = 'friedrich@pudo.org',
    description = 'Track when teachers are not present in school classes.',
    long_description = '''''',
    license = 'MIT',
    url = '',
    download_url = '',
    include_package_data = True,
    entry_points = '''
    '''
)


