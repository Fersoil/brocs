# BRoCS - Graph coloring package

Authors: Jakub Grzywaczewski, Tymoteusz Kwieciński

## Prerequisites

Python version 3.10 or higher

## Install
```bash
pip install .
```

## Install for development

1. Create virtual environment
```bash
python3 -m venv venv
```

2. Activate venv (virtual environment)
```bash
source ./venv/bin/activate
```
or 

```bat
.\venv\bin\activate.bat
```

3. Install package in live code version
```bash
python3 -m pip install -e .
```

## Examples for usage as library:
You can run CS example with
```bash
python3 examples/cs-example.py
```
 as a CLI tool

## Usage as a CLI tool
Start the program by providing the path to stored graphs in the *.npy files

Run on examples:
```bash
brocs graph_files
```

