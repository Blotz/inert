compile and wrap with tbenthompson/cppimport and pybind11, which creates an importable python library

pybind11 included as git submodule in <rootdir>/src/colorapp/pybind11


## In python code

Add c++ file location to python include path. Then import:
```python
import cppimport.import_hook
import colorapp.cpp
```
Then call ``output=colorapp.recolor(params)``. C++ code will compile on launch when imported and appear as a python module.

#### Expected inputs:
1. pixel data in bytes (raw)
2. image height
3. image width
4. Target rgb in R, G, B order in separate inputs
5. intensity

#### Expected output:
Bytes object readable using Image.frombytes()
