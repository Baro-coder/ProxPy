import setuptools


with open('README.md', ) as file:
    long_description = file.read()


setuptools.setup(
    name='proxpy',
    version='0.0.1',
    author='Szykuła Bartłomiej',
    author_email='b.szykula00@gmail.com',
    description='Python module for getting valid free proxy servers list and making requests',
    long_description=long_description,
    url='https://github.com/Baro-coder/ProxPy',
    packages=setuptools.find_packages(),
    package_data={"proxpy" : ['user-agents_list.txt']},
    requires=[
        'beautifulsoup4==4.12.2',
        'bs4==0.0.1',
        'soupsieve==2.4.1'
        ],
    license='MIT License',
    keywords='python proxies proxy proxylist'
)