"""Import checks for the preprocessing module."""

import importlib


def test_preprocessing_module_imports() -> None:
    """The preprocessing module should be importable from the project package."""
    module = importlib.import_module("src.preprocessing")

    assert module is not None
