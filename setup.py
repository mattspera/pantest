import setuptools

setuptools.setup(
    name='pantest',
    version='0.0.1',
    description='A Palo Alto Networks Python Testing Suite',
    author='Matthew Spera',
    author_email='speramatthew@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'xmltodict'
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
)