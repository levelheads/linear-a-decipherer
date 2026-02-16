"""Smoke tests: verify key modules import without errors."""

import importlib
import py_compile
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"


def test_tools_directory_exists():
    assert TOOLS_DIR.is_dir(), f"tools/ directory not found at {TOOLS_DIR}"


def test_tools_compile():
    """All .py files in tools/ should pass py_compile."""
    failures = []
    for py_file in sorted(TOOLS_DIR.glob("*.py")):
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            failures.append(str(e))
    assert not failures, "Compilation failures:\n" + "\n".join(failures)


def test_key_modules_import():
    """Core modules should be importable.

    Tools use intra-package imports (e.g. `import word_filter_contract`),
    so we add the tools/ directory itself to sys.path.
    """
    sys.path.insert(0, str(TOOLS_DIR.parent))
    sys.path.insert(0, str(TOOLS_DIR))
    modules = [
        "tools.parse_lineara_corpus",
        "tools.hypothesis_tester",
        "tools.validate_corpus",
        "tools.anchor_tracker",
    ]
    failures = []
    for mod in modules:
        try:
            importlib.import_module(mod)
        except Exception as e:
            failures.append(f"{mod}: {e}")
    assert not failures, "Import failures:\n" + "\n".join(failures)
