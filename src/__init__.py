"""reddit-digest pipeline package.

Warning filter lives here because __init__ runs before any submodule import —
registering it inside a submodule was too late when a sibling imported the
google client first.
"""

import warnings

# google-api-core emits a Python-3.10 deprecation FutureWarning on import.
# It is pure noise that otherwise has to be grepped out of every script's output.
warnings.filterwarnings("ignore", message=r".*Python version.*", category=FutureWarning)
