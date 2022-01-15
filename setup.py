#!/usr/bin/env python3

import setuptools
from pathlib import Path
import sys

name = "frozendict"
main_package_name = "frozendict"
test_dir_name = "test"
readme_filename = "README.md"
version_filename = "VERSION"
py_typed_filename = "py.typed"
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

main_package_path = curr_dir / main_package_name

version = ""
version_path = main_package_path / version_filename

with open(version_path) as f:
    version = f.read()

excluded_packages = (test_dir_name, )
packages = setuptools.find_packages(exclude=excluded_packages)
package_data_filenames = (version_filename, py_typed_filename)
package_data = {package_name: package_data_filenames for package_name in packages}

# C extension - START

src_dir_name = "src"
src_base_path = main_package_path / src_dir_name
include_dir_name = "Include"

ext1_name = "_" + name
ext1_fullname = main_package_name + "." + ext1_name
ext1_source1_name = name + "object"
ext1_source1_fullname = ext1_source1_name + ".c"

cpython_objects_dir_name = "Objects"
cpython_stringlib_name = "stringlib"
cpython_objects_clinic_name = "clinic"

extra_compile_args = ["-DPY_SSIZE_T_CLEAN", ]

pyversion = sys.version_info

cpython_version = f"{pyversion[0]}_{pyversion[1]}"

src_path = src_base_path / cpython_version

cpython_path = src_path / "cpython_src"
cpython_object_path = cpython_path / cpython_objects_dir_name

include_path = src_path / include_dir_name
cpython_stringlib_path = cpython_object_path / cpython_stringlib_name
cpython_objects_clinic_path = cpython_object_path / cpython_objects_clinic_name

cpython_include_dirs = [
    str(include_path), 
    str(cpython_object_path), 
    str(cpython_stringlib_path), 
    str(cpython_objects_clinic_path), 
    str(cpython_path), 
]

ext1_source1_path = src_path / ext1_source1_fullname

cpython_sources_tmp = [ext1_source1_path, ]

cpython_sources = [
    str(x.relative_to(curr_dir))
    for x in cpython_sources_tmp
]

undef_macros = []

argv = sys.argv

if argv[1] == "c_debug":
    undef_macros = ["NDEBUG"]

ext_modules = []

ext_modules.append(setuptools.Extension(
    ext1_fullname,
    sources = cpython_sources,
    include_dirs = cpython_include_dirs,
    extra_compile_args = extra_compile_args,
    undef_macros = undef_macros,
))



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
    package_data = package_data,
    
    description = description,
    long_description = long_description,
    long_description_content_type = readme_content_type,
    
    classifiers = classifiers,
    keywords = keywords,
)

custom_arg = None

custom_args = ("py", "c", "c_debug")

if len(argv) > 1 and argv[1] in custom_args:
    custom_arg = argv[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]

if custom_arg == None:
    custom_arg = "c"

if custom_arg == "py":
    setuptools.setup(**common_setup_args)
elif custom_arg in ("c", "c_debug"):
    setuptools.setup(ext_modules = ext_modules, **common_setup_args)
else:
    raise ValueError(f"Unsupported custom_arg {custom_arg}")
