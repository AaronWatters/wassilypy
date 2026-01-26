"""Wassily Python wrapper - simple hello world example."""

import importlib.resources

__version__ = "0.1.0"


def hello():
    """Return a hello world message."""
    return "Hello, World!"


def load_data():
    """Load the sample data file from the package data directory.
    
    Returns:
        str: Contents of the sample.txt data file.
    """
    try:
        # Python 3.9+
        files = importlib.resources.files('wassilypy')
        data_file = files / 'data' / 'sample.txt'
        return data_file.read_text()
    except AttributeError:
        # Python 3.7-3.8 fallback
        import importlib.resources as resources
        with resources.open_text('wassilypy.data', 'sample.txt') as f:
            return f.read()
