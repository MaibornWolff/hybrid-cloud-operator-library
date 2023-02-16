from distutils.core import setup


setup(
    name="hybrid-cloud-operator-library",
    version="0.1.0",
    description="A library that contains common parts of the different hybrid-cloud operators by MaibornWolff",
    author="MaibornWolff",
    author_email="sebastian.woehrl@maibornwolff.de",
    url="https://github.com/MaibornWolff/hybrid-cloud-operator-library",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=["hybridcloud_core", "hybridcloud_core/configuration", "hybridcloud_core/k8s", "hybridcloud_core/operator"],
    install_requires=[
        "kubernetes==26.1.0",
        "kopf==1.36.0",
        "pyyaml==6.0",
    ],
)
