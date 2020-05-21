import sys
if sys.version.startswith('3.6'):
    from .py36.libpandadna import *
else:
    if sys.platform == "darwin":
        from .mac.libpandadna import *
    else:
        from .libpandadna import *