# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import sys
from pathlib import Path
from shutil import copytree

sourcedir = Path(__file__).parent.resolve()
docsdir = sourcedir.parent
builddir = docsdir / "build"
basedir = docsdir.parent

# Allow finding of modules for building docs
sys.path.insert(0, str(sourcedir / "modules"))

# If we are an insource build, then append the src dir to path
if tags.has("insource"):
    srcdir = basedir / "src"
    sys.path.insert(0, str(srcdir))

# If the cleanpages tag is passed, then delete all the generated pages
if tags.has("cleanpages"):
    if (sourcedir / "pages").exists():
        print("Cleaning pages directory...")
        import shutil

        shutil.rmtree(sourcedir / "pages")
    if (sourcedir / "index.rst").exists():
        print("Cleaning autogenerated index.rst")
        (sourcedir / "index.rst").unlink()

# -- Project information -----------------------------------------------------

project = "endplay"
copyright = "2021, Dominic Price"
author = "Dominic Price"

# Import endplay.
import endplay

print("Using build located at", endplay.__path__[0])
release = endplay.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinxcontrib.apidoc",
    "sphinx.ext.autodoc",
    "myst_parser",
    "autodoc_rename",
    "parse_readme",
    "autodocsumm",
    "generate_index",
]

# apidoc
apidoc_module_dir = endplay.__path__[0]
apidoc_output_dir = str(sourcedir / "pages" / "reference")
apidoc_excluded_paths = []
apidoc_separate_modules = True
apidoc_module_first = True
apidoc_toc_file = False
apidoc_template_dir = str(sourcedir / "_templates")
apidoc_extra_args = ["-P", f"--templatedir={apidoc_template_dir}"]

# autodoc
autodoc_default_options = {"autosummary": True}

# readme
readme_module_dir = str(basedir)
readme_output_dir = str(sourcedir / "pages" / "readme")

# sphinx
templates_path = ["_templates"]
exclude_patterns = ["static_pages"]

# index
index_template_file = sourcedir / "_templates" / "index.rst_t"
index_output_file = sourcedir / "index.rst"
index_pages_root = sourcedir / "pages"
index_sections = [
    "readme",
    "inputformat.md",
    "reference/endplay.rst",
]

# copy everything from 'static_pages' into 'pages'
copytree("static_pages", "pages")

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = [
    "css/split_params.css",
    "css/pretty_toc.css",
]
html_js_files = [
    "js/split_method_params.js",
]

# -- Patch for resolving cross references ------------------------------------

from sphinx.domains.python import PythonDomain


class PythonDomainXref(PythonDomain):
    def find_obj(self, env, modname, classname, name, type, searchmode=0):
        """
        If multiple locations for an object are found, then resolve to the most
        specific
        """
        orig_matches = PythonDomain.find_obj(
            self, env, modname, classname, name, type, searchmode
        )
        if len(orig_matches) <= 1:
            return orig_matches
        longest_match, length = None, 0
        for match in orig_matches:
            if len(match[0]) > length:
                longest_match, length = match, len(match[0])
        return [longest_match]


def setup(sphinx):
    sphinx.add_domain(PythonDomainXref, override=True)
