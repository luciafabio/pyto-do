from setuptools import setup, find_packages
setup(
    name="pytodo",
    version="0.0.1",
    python_requires=">=3.9.0",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": ["td = pytodo:entry_point"]
    },)
