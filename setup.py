from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))


setup(
    name="multicall-py",
    version="1.3.3",
    description="Ethereum multiple contract/rpc calls",
    long_description=open(os.path.join(here, "README.md")).read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="ethereum jsonrpc contract",
    author="Wenbiao Zheng",
    author_email="delweng@gmail.com",
    url="https://github.com/jsvisa/multicall.py",
    license="MIT",
    packages=find_packages(include=["multicall"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "eth-abi>=4.1.0",
        "requests",
    ],
)
