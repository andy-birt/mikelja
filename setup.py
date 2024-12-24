from setuptools import setup, find_packages

setup(
    name="mikelja",
    version="0.0.1",
    description="A Python library to aggregate job listings from various APIs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andrew Birt",
    author_email="andrew.birt@proton.me",
    url="https://github.com/andy-birt/mikelja",
    python_requires=">=3.7",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)