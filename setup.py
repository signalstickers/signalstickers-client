import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signalstickers-client",
    version="3.2.0",
    author="Romain Ricard",
    author_email="contact+stickerclient@romainricard.fr",
    description="A client for the Signal stickers API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/romainricard/signalstickers-client",
    packages=setuptools.find_packages(),
    install_requires=[
        'anyio>=2.0.2,<3.0.0',
        'httpx>=0.16.1,<0.17.0',
        'cryptography>=3.1.1,<4.0.0',
        'protobuf>=3.13.0,<4.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat"
    ],
    python_requires='>=3.6',
    package_data={
        'signalstickers_client': ['utils/ca/cacert.pem']
    }
)
