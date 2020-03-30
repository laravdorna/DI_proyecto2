import setuptools

with open('app/requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='ID_proyecto',
    version='0.1',
    author="Lara Vazquez",
    author_email="lvazquezdorna@danielcastelao.org",
    description="Aplicación de tienda en GTK",
    url="https://github.com/laravdorna/DI_proyecto2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: UNIX",
    ],
    package_data={'app': [
        'app.db',
        'requirements.txt',
        'Glade/*.glade',
    ]},
    install_requires=requirements,
    scripts=[
        'app/main.py'
    ],
    entry_points = {
        'console_scripts': ['id_proyecto=app.main:main']
    }
)
