![PySlidesGenerator Logo](https://mauricelambert.github.io/info/python/code/PySlidesGenerator_small.png "PySlidesGenerator logo")

# PySlidesGenerator

## Description

**A powerful GUI for creating HTML-based "hacker-style" presentation slides**

Generate visually striking presentations through an intuitive interface with extensive customization options. Easily create and manage slides featuring titles, subtitles, speaker notes, images, code snippets with syntax highlighting, references and sources, animations, and much more.

Designed for technical talks, cybersecurity demonstrations, developer conferences, and educational content, this tool allows you to build professional-looking HTML slide decks while adapting the visual style to your needs—from minimalist terminal aesthetics to fully customized hacker-inspired themes.

**Features**

 - 🎨 Multiple customizable visual themes and styles
 - 📝 Speaker notes support
 - 📌 Titles and subtitles management
 - 🖼️ Image integration
 - 💻 Code block support with syntax highlighting
 - 📚 References and source citations
 - ✨ Built-in animations and transitions
 - ⚙️ Easy slide configuration through a graphical interface
 - 🌐 HTML output for maximum portability

Create engaging, technical, and visually impactful presentations without manually editing HTML files.


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
