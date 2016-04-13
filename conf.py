#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# DFHack documentation build configuration file
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import fnmatch
from io import open
import os
import shlex
import sys


# -- Autodoc for DFhack scripts -------------------------------------------

def doc_dir(dirname, files):
    """Yield (command, includepath) for each script in the directory."""
    sdir = os.path.relpath(dirname, '.').replace('\\', '/').replace('../', '')
    for f in files:
        if f[-3:] not in ('lua', '.rb'):
            continue
        with open(os.path.join(dirname, f), 'r', encoding='utf8') as fstream:
            text = [l.rstrip() for l in fstream.readlines() if l.strip()]
        command = None
        for line in text:
            if command and line == len(line) * '=':
                yield command, sdir + '/' + f
                break
            command = line


def document_scripts():
    """Autodoc for files with the magic script documentation marker strings.

    Creates a file for eack kind of script (base/devel/fix/gui/modtools)
    with all the ".. include::" directives to pull out docs between the
    magic strings.
    """
    # First, we collect the commands and paths to include in our docs
    scripts = []
    for root, _, files in os.walk('scripts'):
        scripts.extend(doc_dir(root, files))
    # Next we split by type and create include directives sorted by command
    kinds = {'base': [], 'devel': [], 'fix': [], 'gui': [], 'modtools': []}
    for s in scripts:
        k_fname = s[0].split('/', 1)
        if len(k_fname) == 1:
            kinds['base'].append(s)
        else:
            kinds.get(k_fname[0], []).append(s)
    template = ('.. _{}:\n\n'
                '.. include:: /{}\n'
                '   :start-after: =begin\n'
                '   :end-before: =end\n')
    for key, value in kinds.items():
        kinds[key] = [template.format(x[0], x[1])
                      for x in sorted(value, key=lambda x: x[0])]
    # Finally, we write our _auto/* files for each kind of script
    if not os.path.isdir('docs/_auto'):
        os.mkdir('docs/_auto')
    head = {
        'base': 'Basic Scripts',
        'devel': 'Development Scripts',
        'fix': 'Bugfixing Scripts',
        'gui': 'GUI Scripts',
        'modtools': 'Scripts for Modders'}
    for k in head:
        title = ('.. _{k}:\n\n{l}\n{t}\n{l}\n\n'
                 '.. include:: /scripts/{a}about.txt\n\n'
                 '.. contents::\n\n').format(
            k=k, t=head[k], l=len(head[k])*'#', a=('' if k=='base' else k+'/'))
        mode = 'w' if sys.version_info.major > 2 else 'wb'
        with open('docs/_auto/{}.rst'.format(k), mode) as outfile:
            outfile.write(title)
            outfile.write('\n\n'.join(kinds[k]))


# Actually call the docs generator
document_scripts()


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.3'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.extlinks']

# This config value must be a dictionary of external sites, mapping unique
# short alias names to a base URL and a prefix.
# See http://sphinx-doc.org/ext/extlinks.html
extlinks = {
    'wiki': ('http://dwarffortresswiki.org/%s', ''),
    'forums': ('http://www.bay12forums.com/smf/index.php?topic=%s',
               'Bay12 forums thread '),
    'dffd': ('http://dffd.bay12games.com/file.php?id=%s', 'DFFD file '),
    'bug': ('http://www.bay12games.com/dwarves/mantisbt/view.php?id=%s',
            'Bug '),
    'issue': ('https://github.com/DFHack/dfhack/issues/%s', 'Issue '),
    'commit': ('https://github.com/DFHack/dfhack/commit/%s', 'Commit '),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst']

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'DFHack'
copyright = '2015, The DFHack Team'
author = 'The DFHack Team'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

def get_version():
    """Return the DFHack version string, from CMakeLists.txt"""
    version = release = ''
    try:
        with open('CMakeLists.txt') as f:
            for s in f.readlines():
                if fnmatch.fnmatch(s.upper(), 'SET(DF_VERSION "?.??.??")\n'):
                    version = s.upper().replace('SET(DF_VERSION "', '')
                elif fnmatch.fnmatch(s.upper(), 'SET(DFHACK_RELEASE "r*")\n'):
                    release = s.upper().replace('SET(DFHACK_RELEASE "', '').lower()
        return (version + '-' + release).replace('")\n', '')
    except IOError:
        return 'unknown'

# The short X.Y version.
# The full version, including alpha/beta/rc tags.
version = release = get_version()

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    'README.md',
    'docs/html*',
    'depends/*',
    'scripts/3rdparty/*',
    'build*',
    ]

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'ref'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'
html_style = 'dfhack.css'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    #'logo': 'logo.png',
    'github_user': 'DFHack',
    'github_repo': 'dfhack',
    'github_button': False,
    'travis_button': False,
}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = 'DFHack Docs'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'docs/styles/dfhack-icon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['docs/styles']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%d'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': [
        'about.html',
        'relations.html',
        'searchbox.html',
        'localtoc.html',
    ]
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = False

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'DFHackdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',

# Latex figure (float) alignment
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'DFHack.tex', 'DFHack Documentation',
   'The DFHack Team', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'dfhack', 'DFHack Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'DFHack', 'DFHack Documentation',
   author, 'DFHack', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False