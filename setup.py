import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chip_eight-apalmer", 
    version="0.0.3",
    author="Adigun Palmer",
    author_email="adigunpalmer@hotmail.com",
    description="CHIP-8 Emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apalmer/chip_eight",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)