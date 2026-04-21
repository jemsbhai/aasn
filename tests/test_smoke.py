"""Smoke tests for aasn package."""

from aasn import __version__


def test_version_exists():
    """Verify the package version is set."""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_package_imports():
    """Verify core subpackages are importable."""
    import aasn.core
    import aasn.dna
    import aasn.registry
    import aasn.compiler
    import aasn.adapters
    import aasn.evolution
    import aasn.plugins
    import aasn.testing
    import aasn.observability
