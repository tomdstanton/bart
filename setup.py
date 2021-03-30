from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('bart/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as rm:
    long_description = rm.read()

setup(
    name="bart",
    version=main_ns['__version__'],
    author="Tom Stanton",
    author_email="tomdstanton@gmail.com",
    description="Quickly find MLST profile and genes of interest in bacterial short reads",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    include_package_data = True,
    package_data={'bart': ['bart/db/scheme_species_map.tab']},
    scripts=['bart/bart'],
    keywords='microbial genomics amr virulence',
    install_requires=requirements,
    zip_safe=False
)
