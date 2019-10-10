#!/usr/bin/env python3

import setuptools
from pathlib import Path
import mimetypes

test_dir_name = "test"
readme_filename = "README.md"
main_url = "https://github.com/Marco-Sulla/python-frozendict"

curr_path = Path(__file__).resolve()
curr_dir = curr_path.parent
readme_path = curr_dir / readme_filename

readme_content_type = mimetypes.guess_type(str(readme_path), strict=False)[0]
excluded_packages = (test_dir_name, )

long_description = ""

with open(readme_path) as f:
	long_description = f.read()

setuptools.setup(
    name = "frozendict",
    author = "Marco Sulla",
    author_email = "marcosullaroma@gmail.com",
    version = "1.0",
    license  = "LGPL v3",
    url = main_url,
    packages = setuptools.find_packages(exclude=excluded_packages),

    description = "An immutable dictionary",
    long_description = long_description,
    long_description_content_type = readme_content_type,

    classifiers = [
    	"Development Status :: 5 - Production/Stable",
    	"Intended Audience :: Developers",
    	"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    	"Programming Language :: Python :: 3 :: Only",
    	"Natural Language :: English", 
    	"Operating System :: OS Independent", 
    	"Topic :: Software Development :: Libraries",
    	"Topic :: Software Development :: Libraries :: Python Modules",
    	"Topic :: Utilities", 
    ],

    keywords = "immutable hashable picklable frozendict dict dictionary map Mapping MappingProxyType developers stable utility",
    python_requires = ">=3.4",

    project_urls = {
        "Bug Reports": "https://github.com/Marco-Sulla/python-frozendict/issues",
        "Source": main_url,
    },
)
