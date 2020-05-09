import sys
if sys.platform == "darwin":
    from .mac.libpandadna import *
else:
    from .libpandadna import *
