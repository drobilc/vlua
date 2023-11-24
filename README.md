# Vlua

A tool for converting Lua code into visual representations for enhanced program comprehension.

## Installation

To install, make sure that you are using at least **Python 3.6**.

```bash
# Install project requirements
pip install -r requirements.txt
```

## Usage

To use, pass the path to the input Lua file as first argument and the output file as an optional argument. If output file is not defined, the generated HTML will be written to the standard output (the console).

```bash
python vlua.py examples/factorial.lua --output-file factorial.html
```
or for a bigger lua source file:
```bash
python vlua.py examples/transform.lua --output-file transform.html
```
The generated HTML will link to `style.css` and apply that style when openend in a browser. 