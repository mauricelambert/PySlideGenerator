![PySlidesGenerator Logo](https://mauricelambert.github.io/info/python/code/PySlidesGenerator_small.png "PySlidesGenerator logo")

# PySlidesGenerator

## Description

Little GUI to generate my slides.

## Requirements

This package require:

 - python3
 - python3 Standard Library

## Installation

### Git

```bash
git clone "https://github.com/mauricelambert/PySlidesGenerator.git"
cd "PySlidesGenerator"
python3 -m pip install .
```

### Wget

```bash
wget https://github.com/mauricelambert/PySlidesGenerator/archive/refs/heads/main.zip
unzip main.zip
cd PySlidesGenerator-main
python3 -m pip install .
```

### cURL

```bash
curl -O https://github.com/mauricelambert/PySlidesGenerator/archive/refs/heads/main.zip
unzip main.zip
cd PySlidesGenerator-main
python3 -m pip install .
```

## Usages

### Command line

```bash
PySlidesGenerator              # Using CLI package executable
python3 -m PySlidesGenerator   # Using python module
python3 PySlidesGenerator.pyz  # Using python executable
PySlidesGenerator.exe          # Using python Windows executable
```

### Python script

```python
from PySlidesGenerator import *

root = Tk()
app = SlideGeneratorApp(root)
root.mainloop()
```

## Links

 - [Github](https://github.com/mauricelambert/PySlidesGenerator)
 - [Documentation](https://mauricelambert.github.io/info/python/code/PySlidesGenerator.html)
 - [Python executable](https://mauricelambert.github.io/info/python/code/PySlidesGenerator.pyz)
 - [Python Windows executable](https://mauricelambert.github.io/info/python/code/PySlidesGenerator.exe)

## License

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
