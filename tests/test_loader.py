"""Import checks for the dataset loading module."""

import importlib


def test_loader_module_imports() -> None:
    """The loader module should be importable from the project package."""
    module = importlib.import_module("src.loader")

    assert module is not None
