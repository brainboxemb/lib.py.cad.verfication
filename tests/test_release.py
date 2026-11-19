from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "publish_release.py"
SPEC = spec_from_file_location("cad_verification_publish_release", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load release script: {SCRIPT}")
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

release_version = MODULE.release_version
version_changed = MODULE.version_changed


class ReleaseTests(unittest.TestCase):
    def make_root(
        self,
        root: Path,
        version: str,
        package_version: str | None = None,
        changelog_version: str | None = None,
    ) -> None:
        package_version = package_version or version
        changelog_version = changelog_version or version
        (root / "VERSION").write_text(version + "\n", encoding="utf-8")
        (root / "pyproject.toml").write_text(
            f'version = "{package_version}"\n',
            encoding="utf-8",
        )
        (root / "CHANGELOG.md").write_text(
            f"# Changelog\n\n## {changelog_version}\n",
            encoding="utf-8",
        )

    def test_release_version_checks_all_version_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_root(root, "0.1.0")
            self.assertEqual(release_version(root), "0.1.0")

    def test_invalid_version_is_not_releasable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_root(root, "0.1.0-dev")
            with self.assertRaisesRegex(ValueError, "not a release version"):
                release_version(root)

    def test_package_version_must_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_root(root, "0.1.0", package_version="0.1.1")
            with self.assertRaisesRegex(ValueError, "do not match"):
                release_version(root)

    def test_changelog_section_must_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_root(root, "0.1.0", changelog_version="0.0.9")
            with self.assertRaisesRegex(ValueError, "has no 0.1.0"):
                release_version(root)

    def test_version_changed_detects_only_version_commits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.name", "test"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=root,
                check=True,
            )

            self.make_root(root, "0.1.0")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "initial"],
                cwd=root,
                check=True,
            )
            self.assertTrue(version_changed(root))

            (root / "README.md").write_text("docs\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "docs"],
                cwd=root,
                check=True,
            )
            self.assertFalse(version_changed(root))

            (root / "VERSION").write_text("0.2.0\n", encoding="utf-8")
            subprocess.run(["git", "add", "VERSION"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "release"],
                cwd=root,
                check=True,
            )
            self.assertTrue(version_changed(root))


if __name__ == "__main__":
    unittest.main()
