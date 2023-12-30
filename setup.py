#!/usr/bin/env python3

import setuptools
from pathlib import Path
import sys
from platform import python_implementation
from os import environ

name = "frozendict"
module1_name = "frozendict"
readme_filename = "README.md"
version_filename = "version.py"
py_typed_filename = "py.typed"
mypy_filename = "__init__.pyi"
main_url = "https://github.com/Marco-Sulla/python-frozendict"
bug_url = "https://github.com/Marco-Sulla/python-frozendict/issues"
author = "Marco Sulla"
author_email = "marcosullaroma@gmail.com"
license  = "LGPL v3"
license_files = "LICENSE.txt"
description = "A simple immutable dictionary"
keywords = "immutable hashable picklable frozendict dict dictionary map Mapping MappingProxyType developers stable utility"
python_requires = ">=3.6"

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6", 
    "Natural Language :: English", 
    "Operating System :: OS Independent", 
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities", 
]

curr_path = Path(__file__).resolve()
curr_dir = curr_path.parent

readme_path = curr_dir / readme_filename
readme_content_type = "text/markdown"

long_description = ""

with open(readme_path) as f:
    long_description = f.read()

package_dir_name = "src"
package_path = curr_dir / package_dir_name

module1_dir_name = module1_name
module1_path = package_path / module1_dir_name

version_path = module1_path / version_filename

with open(version_path) as f:
    # create the version var
    exec(f.read())

package_path_str = str(package_path)
packages = setuptools.find_packages(where = package_path_str)
package_data_filenames = (py_typed_filename, mypy_filename)
package_data = {package_name: package_data_filenames for package_name in packages}

# C extension - START

c_src_dir_name = "c_src"
c_src_base_path = module1_path / c_src_dir_name
include_dir_name = "Include"

ext1_name = "_" + name
ext1_fullname = module1_name + "." + ext1_name
ext1_source1_name = name + "object"
ext1_source1_fullname = ext1_source1_name + ".c"

cpython_objects_dir_name = "Objects"
cpython_stringlib_name = "stringlib"
cpython_objects_clinic_name = "clinic"

extra_compile_args = ["-DPY_SSIZE_T_CLEAN", ]

pyversion = sys.version_info

cpython_version = f"{pyversion[0]}_{pyversion[1]}"

c_src_path = c_src_base_path / cpython_version

cpython_path = c_src_path / "cpython_src"
cpython_object_path = cpython_path / cpython_objects_dir_name

include_path = c_src_path / include_dir_name
cpython_stringlib_path = cpython_object_path / cpython_stringlib_name
cpython_objects_clinic_path = cpython_object_path / cpython_objects_clinic_name

cpython_include_dirs = [
    str(include_path), 
    str(cpython_object_path), 
    str(cpython_stringlib_path), 
    str(cpython_objects_clinic_path), 
    str(cpython_path), 
]

ext1_source1_path = c_src_path / ext1_source1_fullname

cpython_sources_tmp = [ext1_source1_path, ]

cpython_sources = [
    str(x.relative_to(curr_dir))
    for x in cpython_sources_tmp
]

undef_macros = []

argv = sys.argv
argv_1_exists = len(argv) > 1

if argv_1_exists and argv[1] == "c_debug":
    undef_macros = ["NDEBUG"]

def get_ext_module(
    fullname, 
    sources, 
    include_dirs, 
    extra_compile_args,
    undef_macros,
    optional
):
    ext_module = setuptools.Extension(
        fullname,
        sources = sources,
        include_dirs = include_dirs,
        extra_compile_args = extra_compile_args,
        undef_macros = undef_macros, 
        optional = optional, 
    )
    
    return ext_module

def get_ext_module_1(optional):
    return get_ext_module(
        fullname = ext1_fullname,
        sources = cpython_sources,
        include_dirs = cpython_include_dirs,
        extra_compile_args = extra_compile_args,
        undef_macros = undef_macros, 
        optional = optional, 
    )

# C extension - END

common_setup_args = dict(
    name = name,
    author = author,
    author_email = author_email,
    version = version,
    python_requires = python_requires,
    license  = license,
    license_files = (license_files, ),
    url = main_url,
    
    project_urls = {
        "Bug Reports": bug_url,
        "Source": main_url,
    },
    
    packages = packages,
    package_dir = {"": package_dir_name}, 
    package_data = package_data,
    
    description = description,
    long_description = long_description,
    long_description_content_type = readme_content_type,
    
    classifiers = classifiers,
    keywords = keywords,
)

custom_arg = None

custom_args_py = ("py", )
custom_args_c = ("c", "c_debug")
custom_args = custom_args_py + custom_args_c

if argv_1_exists and argv[1] in custom_args:
    custom_arg = argv[1]
    sys.argv = [argv[0]] + argv[2:]

impl = python_implementation()

# C Extension is optional by default from version 2.3.5
# If the module is built by pipeline, C Extension must be mandatory.
optional = environ.get('CIBUILDWHEEL') != '1'

# Check if build the pure py implementation
pure_py_env = environ.get('FROZENDICT_PURE_PY')
pure_py = pure_py_env == '1'

mix_c_py_error = ValueError(
    "You can't specify the pure py implementation *and* C extension togheter"
)

if custom_arg == None:
    if impl == "PyPy" or not c_src_path.exists():
        custom_arg = "py"
    else:
        custom_arg = "py" if pure_py else "c"
elif custom_arg in custom_args_c:
    if pure_py:
        raise mix_c_py_error
    
    optional = False

if pure_py and not optional:
    raise mix_c_py_error

if custom_arg in custom_args_py:
    # check if pure py explicitly disabled
    if pure_py_env == '0':
        raise mix_c_py_error
    
    setuptools.setup(**common_setup_args)
elif custom_arg in custom_args_c:
    ext_module_1 = get_ext_module_1(optional)
    ext_modules = [ext_module_1]
    setuptools.setup(ext_modules = ext_modules, **common_setup_args)
else:
    raise ValueError(f"Unsupported custom_arg {custom_arg}")
