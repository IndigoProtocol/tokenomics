from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()


with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()


setup(
    name="indy-tokenomics",
    version="0.0.0",
    author="Indigo Labs",
    description="An interface for illustrating Indigo’s tokenomics",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[req for req in requirements if req[:2] != "# "],
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "indy=tokenomics.cli:tokenomics",
        ],
    },
)
