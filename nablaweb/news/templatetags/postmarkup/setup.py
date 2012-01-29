"""BBCode to (X)HTML rendering engine

Converts BBCode (http://en.wikipedia.org/wiki/BBCode) in to HTML and
XHTML snippets. Always outputs valid XHTML, even from badly nested BBCode.
"""

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Programming Language :: Python
License :: OSI Approved :: Python Software Foundation License
Operating System :: OS Independent
Topic :: Text Processing :: Markup
"""

from distutils.core import setup
from postmarkup import __version__

doclines = __doc__.split("\n")

setup( name='postmarkup',
       version = __version__,
       author = 'Will McGugan',
       author_email = 'will@willmcgugan.com',
       license = "Python Software Foundation License",
       url = 'http://code.google.com/p/postmarkup/',
       download_url = 'http://code.google.com/p/postmarkup/downloads/list',
       platforms = ['any'],
       description = doclines[0],
       long_description = '\n'.join(doclines[2:]),
       py_modules = ['postmarkup'],
       classifiers = classifiers.splitlines(),
       )
