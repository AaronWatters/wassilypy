"""Tests for the load_data function."""
import wassilypy


def test_load_data():
    """Test that load_data() loads the sample data file correctly."""
    data = wassilypy.load_data()
    assert data is not None, "load_data() should return data"
    assert "Hello from data file!" in data, "Data should contain expected content"
    assert isinstance(data, str), "load_data() should return a string"
