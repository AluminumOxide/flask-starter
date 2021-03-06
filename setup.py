from setuptools import find_packages, setup

setup(
        name='src',
        version='2',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'flask',
            'flask-babel',
            'flask-sqlalchemy',
            'passlib'
        ],
        extras_require={
            'test': [
                'pytest',
                'coverage'
            ]
        }
)
