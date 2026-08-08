"""Tests for the multi-agent skill installer."""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

import install_skills


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.source = self.root / "source"
        self.home = self.root / "home"
        self.source.mkdir()

        for name in ("beta-reviewer", "alpha-reviewer"):
            skill = self.source / name
            skill.mkdir()
            (skill / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
            (skill / "README.md").write_text("documentation\n", encoding="utf-8")

        ignored = self.source / "not-a-skill"
        ignored.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_finds_only_skills_in_stable_order(self) -> None:
        names = [path.name for path in install_skills.find_skills(self.source)]
        self.assertEqual(names, ["alpha-reviewer", "beta-reviewer"])

    def test_default_agents_use_documented_personal_locations(self) -> None:
        destinations = install_skills.target_directories(
            self.home, install_skills.selected_agents(None)
        )
        self.assertEqual(destinations["claude"], self.home / ".claude/skills")
        self.assertEqual(destinations["codex"], self.home / ".agents/skills")
        self.assertEqual(destinations["pi"], self.home / ".pi/agent/skills")
        self.assertEqual(destinations["copilot"], self.home / ".copilot/skills")

    def test_detects_supported_platforms(self) -> None:
        cases = (
            ("Windows", "11", {}, "Windows"),
            ("Darwin", "25.0", {}, "macOS"),
            ("Linux", "6.8.0-generic", {}, "Linux"),
            ("Linux", "5.15.0-microsoft-standard-WSL2", {}, "WSL"),
            ("Linux", "6.8.0-generic", {"WSL_DISTRO_NAME": "Ubuntu"}, "WSL"),
        )

        for system, release, environment, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    install_skills.detect_platform(system, release, environment),
                    expected,
                )

    def test_dry_run_writes_nothing(self) -> None:
        skills = install_skills.find_skills(self.source)
        destinations = install_skills.target_directories(self.home, ["claude"])

        results = install_skills.install(skills, destinations, dry_run=True)

        self.assertFalse(self.home.exists())
        self.assertEqual(results["claude"]["alpha-reviewer"], "would install")

    def test_installs_selected_skill_for_selected_agents(self) -> None:
        available = install_skills.find_skills(self.source)
        skills = install_skills.selected_skills(available, ["beta-reviewer"])
        destinations = install_skills.target_directories(
            self.home, ["claude", "copilot"]
        )

        install_skills.install(skills, destinations)

        for target in destinations.values():
            self.assertEqual(
                (target / "beta-reviewer/SKILL.md").read_text(encoding="utf-8"),
                "# beta-reviewer\n",
            )
            self.assertFalse((target / "alpha-reviewer").exists())

    def test_existing_skill_is_preserved_without_force(self) -> None:
        skill = install_skills.find_skills(self.source)[0]
        target = self.home / ".claude/skills"
        existing = target / skill.name
        existing.mkdir(parents=True)
        (existing / "local.txt").write_text("keep me\n", encoding="utf-8")

        results = install_skills.install([skill], {"claude": target})

        self.assertTrue((existing / "local.txt").exists())
        self.assertEqual(results["claude"][skill.name], "skipped (already exists)")

    def test_force_replaces_only_the_selected_skill(self) -> None:
        skill = install_skills.find_skills(self.source)[0]
        target = self.home / ".claude/skills"
        existing = target / skill.name
        unrelated = target / "another-skill"
        existing.mkdir(parents=True)
        unrelated.mkdir()
        (existing / "stale.txt").write_text("old\n", encoding="utf-8")
        (unrelated / "keep.txt").write_text("keep\n", encoding="utf-8")

        results = install_skills.install([skill], {"claude": target}, force=True)

        self.assertFalse((existing / "stale.txt").exists())
        self.assertTrue((existing / "SKILL.md").exists())
        self.assertTrue((unrelated / "keep.txt").exists())
        self.assertEqual(results["claude"][skill.name], "replaced")

    def test_unknown_skill_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown skill"):
            install_skills.selected_skills(
                install_skills.find_skills(self.source), ["missing-reviewer"]
            )

    def test_repository_skill_metadata_is_portable(self) -> None:
        for skill in install_skills.find_skills():
            with self.subTest(skill=skill.name):
                content = (skill / "SKILL.md").read_text(encoding="utf-8")
                frontmatter = content.split("---", 2)[1]
                fields = {
                    match.group(1): match.group(2)
                    for match in re.finditer(
                        r"^([a-z][a-z-]*):\s*(.+)$", frontmatter, re.MULTILINE
                    )
                }
                self.assertEqual(fields["name"], skill.name)
                self.assertEqual(fields["license"], "MIT")
                self.assertNotIn("[", fields.get("allowed-tools", ""))


if __name__ == "__main__":
    unittest.main()
