import re
from pathlib import Path


def _parse_version(path: Path, pattern: str) -> str:
    content = path.read_text()
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        raise AssertionError(f"No version match found in {path}")
    return match.group(1).strip()


def _normalize(version: str) -> str:
    return version.lstrip("vV")


def test_version_metadata_alignment():
    root = Path(__file__).resolve().parent.parent
    pyproject = root / "pyproject.toml"
    citation = root / "CITATION.cff"
    changelog = root / "linear-a-decipherer" / "CHANGELOG.md"

    py_version = _parse_version(pyproject, r'^version\s*=\s*"([^"]+)"')
    citation_version = _parse_version(citation, r'^version:\s*["\']?([^"\'\n]+)')
    changelog_version = _parse_version(changelog, r"^##\s*[^\(]+\(\s*(v[\d\.]+)")

    normalized = {
        "pyproject": _normalize(py_version),
        "citation": _normalize(citation_version),
        "changelog": _normalize(changelog_version),
    }
    assert len(set(normalized.values())) == 1, (
        "Version metadata must match:\n"
        f"pyproject={py_version}, citation={citation_version}, changelog={changelog_version}"
    )
