from setuptools import setup, find_packages

setup(
    name="shoopack",
    version="0.0.0-alpha",
    packages=find_packages(),
    install_requires=[
        "pyzmq",
    ],
    author="zygn",
    description="Unified IPC layer for Pub/Sub messaging (ZMQ, Redis)",
    python_requires=">=3.8",
)