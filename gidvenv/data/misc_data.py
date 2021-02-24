PIP_CLI_OPTIONS = ['-e',
                   '--editable',
                   '-f',
                   '--find-links',
                   '--require-hashes',
                   '--no-clean',
                   '--pre',
                   '--no-deps',
                   '--user',
                   '-U',
                   '--upgrade',
                   '--force-reinstall',
                   '--no-build-isolation',
                   '--use-pep517',
                   '--no-cache-dir']


VERSION_SPECIFIERS = ['==',
                      '>=',
                      '<=',
                      '>',
                      '<',
                      '~=',
                      '~',
                      '!=']

VERSION_SPECIFIERS = sorted(VERSION_SPECIFIERS, key=len, reverse=True)


SIMPLE_PYPI_URL = "https://pypi.org/simple/"
