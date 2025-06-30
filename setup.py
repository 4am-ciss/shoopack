from setuptools import setup, find_packages

setup(
    name="shoupan",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyzmq",
        "redis",
    ],
    author="zygn",
    description="Unified IPC layer for Pub/Sub messaging (ZMQ, Redis)",
    python_requires=">=3.8",
)