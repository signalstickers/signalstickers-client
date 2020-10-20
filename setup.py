import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signalstickers-client",
    version="3.0.0",
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
    extras_require={'dev': [
        'pytest>=6.1.1,<7.0.0',
        # For some reason we can't add a requirement with extras here
        # if the same requirement is already in `install_requires`.
        # So these have to be copied from anyio[curio,trio].
        # These are here for testing, as pytest-anyio will run the same tests
        # across all three async frameworks.
        'curio>=1.4',
        'trio>=0.16',
    ]},
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
