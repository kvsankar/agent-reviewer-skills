#!/usr/bin/env python3
"""Install this repository's skills for supported coding agents."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import tempfile
from pathlib import Path
from typing import Iterable, Mapping, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parent

# These are the documented personal skill directories for each agent. Copilot's
# directory is shared by its VS Code agent mode and CLI.
AGENT_DESTINATIONS = {
    "claude": Path(".claude/skills"),
    "codex": Path(".agents/skills"),
    "pi": Path(".pi/agent/skills"),
    "copilot": Path(".copilot/skills"),
}


def detect_platform(
    system: str | None = None,
    release: str | None = None,
    environment: Mapping[str, str] | None = None,
) -> str:
    """Return a friendly name for the current supported environment."""
    system = system or platform.system()
    release = release or platform.release()
    environment = os.environ if environment is None else environment

    if system == "Windows":
        return "Windows"
    if system == "Darwin":
        return "macOS"
    if system == "Linux":
        is_wsl = (
            "microsoft" in release.lower()
            or "wsl" in release.lower()
            or "WSL_DISTRO_NAME" in environment
            or "WSL_INTEROP" in environment
        )
        return "WSL" if is_wsl else "Linux"
    return system or "Unknown"


def find_skills(source: Path = REPOSITORY_ROOT) -> list[Path]:
    """Return top-level skill directories in stable name order."""
    return sorted(
        (
            item
            for item in source.iterdir()
            if item.is_dir() and (item / "SKILL.md").is_file()
        ),
        key=lambda item: item.name,
    )


def selected_agents(requested: Sequence[str] | None) -> list[str]:
    """Normalize repeated agent selections and expand the default/all value."""
    if not requested or "all" in requested:
        return list(AGENT_DESTINATIONS)
    return list(dict.fromkeys(requested))


def selected_skills(
    available: Sequence[Path], requested: Sequence[str] | None
) -> list[Path]:
    """Return requested skills or raise with the unknown names."""
    by_name = {skill.name: skill for skill in available}
    if not requested:
        return list(available)

    unknown = sorted(set(requested) - by_name.keys())
    if unknown:
        available_names = ", ".join(sorted(by_name))
        raise ValueError(
            f"unknown skill(s): {', '.join(unknown)}; available: {available_names}"
        )
    return [by_name[name] for name in dict.fromkeys(requested)]


def target_directories(home: Path, agents: Iterable[str]) -> dict[str, Path]:
    """Resolve the personal skill directory for each selected agent."""
    return {agent: home / AGENT_DESTINATIONS[agent] for agent in agents}


def _replace_directory(source: Path, destination: Path) -> None:
    """Copy a skill into place, staging it before replacing an old copy."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}-", dir=destination.parent)
    )
    staged = staging_root / destination.name

    try:
        shutil.copytree(source, staged)
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        elif destination.exists():
            shutil.rmtree(destination)
        staged.rename(destination)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)


def install(
    skills: Sequence[Path],
    destinations: dict[str, Path],
    *,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, dict[str, str]]:
    """Install skills and return per-agent, per-skill status values."""
    results: dict[str, dict[str, str]] = {}

    for agent, target in destinations.items():
        agent_results: dict[str, str] = {}
        for skill in skills:
            destination = target / skill.name
            exists = destination.exists() or destination.is_symlink()

            if exists and not force:
                status = "skipped (already exists)"
            elif dry_run:
                status = "would replace" if exists else "would install"
            else:
                _replace_directory(skill, destination)
                status = "replaced" if exists else "installed"

            agent_results[skill.name] = status
        results[agent] = agent_results

    return results


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Install repository skills for Claude Code, Codex, Pi, and GitHub "
            "Copilot (VS Code agent mode and CLI) on Windows, WSL, macOS, or "
            "Linux."
        )
    )
    parser.add_argument(
        "--agent",
        action="append",
        choices=["all", *AGENT_DESTINATIONS],
        help="target agent; repeat to select several (default: all)",
    )
    parser.add_argument(
        "--skill",
        action="append",
        help="skill directory name; repeat to select several (default: all)",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="home directory under which agent directories are resolved",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace skills that already exist at the destination",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would change without writing files",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list the skills in this repository and exit",
    )
    return parser


def _print_results(
    results: dict[str, dict[str, str]], destinations: dict[str, Path]
) -> None:
    for agent, skill_results in results.items():
        print(f"\n{agent}: {destinations[agent]}")
        for skill_name, status in skill_results.items():
            print(f"  {status:24} {skill_name}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    available = find_skills()

    if args.list:
        for skill in available:
            print(skill.name)
        return 0

    if not available:
        parser.error(f"no top-level skill directories found under {REPOSITORY_ROOT}")

    try:
        skills = selected_skills(available, args.skill)
    except ValueError as error:
        parser.error(str(error))

    agents = selected_agents(args.agent)
    home = args.home.expanduser().resolve()
    destinations = target_directories(home, agents)
    print(f"Platform: {detect_platform()}")
    print(f"Home: {home}")
    results = install(
        skills,
        destinations,
        force=args.force,
        dry_run=args.dry_run,
    )
    _print_results(results, destinations)

    if any(
        status == "skipped (already exists)"
        for agent_results in results.values()
        for status in agent_results.values()
    ):
        print("\nExisting skills were left untouched; use --force to replace them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
