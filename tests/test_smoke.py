"""Smoke tests for aasn package."""

from aasn import __version__


def test_version_exists():
    """Verify the package version is set."""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_package_imports():
    """Verify core subpackages are importable."""
    import aasn.adapters  # noqa: F401
    import aasn.compiler  # noqa: F401
    import aasn.core  # noqa: F401
    import aasn.dna  # noqa: F401
    import aasn.evolution  # noqa: F401
    import aasn.observability  # noqa: F401
    import aasn.plugins  # noqa: F401
    import aasn.registry  # noqa: F401
    import aasn.testing  # noqa: F401
