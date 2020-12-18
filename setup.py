from setuptools import setup, find_packages

import versioneer

setup(
    author='Markus Leist',
    author_email='markus.leist@metronom.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    cmdclass=versioneer.get_cmdclass(),
    description='D3CT Core Tools',
    include_package_data=True,
    license='BSD',
    name='d3ct',
    version=versioneer.get_version(),
    packages=find_packages(),
)
