### Windows
#### Unable to install polyglot of pip dependencies
You may need to manually install PyICU.whl and PyCLD2.whl. Download the appropiate version for your python version and arch from https://www.lfd.uci.edu/~gohlke/pythonlibs/

#### Unable to install libraqm/Right-to-left fonts not properly working
You need to download libraqm DLLs from here:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow

Place them in the same folder as `python.exe` or in some directory registered in the `PYTHONPATH` env variable

### Debian/Ubuntu Linux

#### ModuleNotFoundError: No module named 'tkinter'
Install it using `sudo apt-get install python3-tk`

#### Problems installing libICU / PyICU
PyICU requires the ICU C++ libraries and headers to be installed on your system before it can be built.

**Debian/Ubuntu Linux:**
```bash
sudo apt-get install libicu-dev pkg-config g++
```

**Fedora/RedHat/CentOS:**
```bash
sudo dnf install libicu-devel pkgconf-pkg-config gcc-c++
```

**macOS (Homebrew):**
```bash
brew install icu4c
export PATH="/usr/local/opt/icu4c/bin:/usr/local/opt/icu4c/sbin:$PATH"
export PKG_CONFIG_PATH="/usr/local/opt/icu4c/lib/pkgconfig"
export ICU_VERSION=$(icu-config --version)
export PYICU_INCLUDES=/usr/local/opt/icu4c/include
export PYICU_LFLAGS=-L/usr/local/opt/icu4c/lib
```

After installing the system dependencies, try installing with:
```bash
pip install pyicu
```
or if using poetry:
```bash
poetry install -E languages
```
