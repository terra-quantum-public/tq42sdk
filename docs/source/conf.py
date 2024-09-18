import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
# -- Project information
project = "TQ42SDK"
copyright = "2024, Terra Quantum AG"  # pylint: disable=redefined-builtin
author = "Terra Quantum AG"

release = ""
version = ""

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinxcontrib.apidoc",  # convert .py sources to .rst docs.
    "myst_parser",
]

# sphinxcontrib.apidoc vars
apidoc_module_dir = "../../tq42"
apidoc_output_dir = "."
apidoc_toc_file = False
apidoc_excluded_paths = [
    "functional_tests/*",
    "cli/*",
    "tests/*",
    "utils/*",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "renku"
html_theme_options = {
    "logo_only": True,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    # Toc options
    "collapse_navigation": False,
    "sticky_navigation": False,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
# -- Options for EPUB output
epub_show_urls = "footnote"
