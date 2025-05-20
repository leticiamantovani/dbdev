from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dbdev",
    version="0.1.1", 
    description="A CLI tool to automate SQL database container management for developers using Docker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Leticia Mantovani",
    author_email="leticiamantovani159@email.com",
    url="https://github.com/leticiamantovani/dbdev",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "docker",
        "python-dotenv",
        "typer"
    ],
    entry_points={
        "console_scripts": [
            "dbdev=dbdev.cli:app",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
