import setuptools

setuptools.setup(
    name="respool",
    version="0.0.1",
    author="xiong ke",
    author_email="635261081@qq.com",
    description="一个资源池的小工具",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
    install_requires=[
        # "numpy >= 1.19.5",
        # "pandas",
  ],
    entry_points={
        'console_scripts': []
        }
)