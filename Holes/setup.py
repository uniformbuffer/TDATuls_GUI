import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Holes",
    version="1.0",
    author="lordgrilo",
    author_email="giovanni.petri@isi.it",
    description="A Python module for detecting, analysing and visualising persistent homological features of complex networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lordgrilo/Holes",
    packages=['Holes','Holes/classes','Holes/measures','Holes/operations','Holes/drawing','Holes/perseus_utils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
