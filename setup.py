import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbupy",
    version="1.1",
    author="Miso Mijatovic",
    author_email="mmijatovic@sorint.it",
    description="Module to use the API of Veritas Netbackup ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wecode.sorint.it/SorintSpain/nbupy",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
