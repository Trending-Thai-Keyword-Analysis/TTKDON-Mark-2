from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules= cythonize("lcs_method.pyx",compiler_directives={'language_level': 3}))