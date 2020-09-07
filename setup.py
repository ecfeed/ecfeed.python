import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecfeed", 
    version="2.0.1",
    author="EcFeed AS",
    author_email="mail@ecfeed.com",
    description="Python interface for accessing EcFeed online generator service",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/ecfeed/ecfeed.python",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    keywords = 'testing pairwise test_generation',
    py_modules=['ecfeed', 'ecfeed_cli'],
    install_requires=['pyopenssl', 'requests'],
    entry_points={
        'console_scripts':[
            'ecfeed=ecfeed_cli:main'
        ]
    },
)
