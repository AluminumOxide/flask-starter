from setuptools import find_packages, setup

setup(
        name='src',
        version='1.1.2111432',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=['flask'],
        extras_require={
            'test': [
                'pytest',
                'coverage'
            ]
        }
)
