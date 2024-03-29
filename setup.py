from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('bart/scripts/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="bart",
    version=main_ns['__version__'],
    author="Tom Stanton",
    author_email="tomdstanton@gmail.com",
    description="BActerial Read Typer",
    url="https://github.com/tomdstanton/bart",
    project_urls={
        "Bug Tracker": "https://github.com/tomdstanton/bart/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    scripts=['bart/bart', 'bart/bart-update', 'bart/bart-profile'],
    keywords='microbial genomics amr virulence',
    install_requires='requests',
    zip_safe=False,
)
