from setuptools import setup

setup(
    name="brocs",
    version="0.1",
    author="Tymoteusz Kwieciński, Jakub Grzywaczewski",
    author_email="""
    tymoteusz.kwiecinski.stud@pw.edu.pl,
    jakub.grzywaczewski2.stud@pw.edu.pl
    """,
    description="""
    A Python package for graph coloring using a algorithm 
    derived from the Lovasz's proof of the Brooks' theorem.
    Additionaly it includes CS coloring algorithm 
    """,
    packages=[
        "brocs",
        "brocs.algorithms",
    ],
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas",
        "networkx",
        "scipy"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    entry_points={
        'console_scripts': ['brocs=brocs.main:main']
    }
)
