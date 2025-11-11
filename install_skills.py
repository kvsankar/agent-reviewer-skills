#!/usr/bin/env python3
"""
Install Claude Code skills to both Windows and WSL ~/.claude/skills/ directories.
"""

import os
import shutil
import subprocess
from pathlib import Path


def get_skill_directories():
    """Find all skill directories (containing SKILL.md) in the current directory."""
    current_dir = Path(__file__).parent
    skill_dirs = []

    for item in current_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skill_dirs.append(item)

    return skill_dirs


def copy_skills_to_windows():
    """Copy skills to Windows ~/.claude/skills/ directory."""
    windows_home = Path.home()
    target_dir = windows_home / ".claude" / "skills"

    print(f"\n[*] Installing skills to Windows: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    skill_dirs = get_skill_directories()
    installed = []

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        dest = target_dir / skill_name

        # Remove existing directory if it exists
        if dest.exists():
            shutil.rmtree(dest)

        # Copy the skill directory
        shutil.copytree(skill_dir, dest)
        installed.append(skill_name)
        print(f"  [+] {skill_name}")

    return installed


def copy_skills_to_wsl():
    """Copy skills to WSL ~/.claude/skills/ directory."""
    print(f"\n[*] Installing skills to WSL...")

    # Try to detect WSL
    try:
        # Get WSL username
        result = subprocess.run(
            ["wsl", "echo", "$USER"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            print("  [!] WSL not available or not configured")
            return []

        wsl_user = result.stdout.strip()
        wsl_home = f"/home/{wsl_user}"
        wsl_target = f"{wsl_home}/.claude/skills"

        print(f"  WSL User: {wsl_user}")
        print(f"  Target: {wsl_target}")

        # Create target directory in WSL
        subprocess.run(
            ["wsl", "mkdir", "-p", wsl_target],
            check=True
        )

        skill_dirs = get_skill_directories()
        installed = []

        for skill_dir in skill_dirs:
            skill_name = skill_dir.name

            # Convert Windows path to WSL path format
            # C:\path\to\skill -> /mnt/c/path/to/skill
            windows_path = str(skill_dir.absolute())
            # Convert Windows path to WSL mount path
            drive_letter = windows_path[0].lower()
            wsl_source = f"/mnt/{drive_letter}/{windows_path[3:].replace(os.sep, '/')}"

            wsl_dest = f"{wsl_target}/{skill_name}"

            # Remove existing directory if it exists
            subprocess.run(
                ["wsl", "rm", "-rf", wsl_dest],
                check=False
            )

            # Copy using WSL cp command
            result = subprocess.run(
                ["wsl", "cp", "-r", wsl_source, wsl_dest],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                installed.append(skill_name)
                print(f"  [+] {skill_name}")
            else:
                print(f"  [-] {skill_name} (failed: {result.stderr.strip()})")

        return installed

    except subprocess.TimeoutExpired:
        print("  [!] WSL command timed out")
        return []
    except FileNotFoundError:
        print("  [!] WSL not found (wsl.exe not in PATH)")
        return []
    except Exception as e:
        print(f"  [!] Error accessing WSL: {e}")
        return []


def main():
    print("=" * 60)
    print("Claude Code Skills Installer")
    print("=" * 60)

    skill_dirs = get_skill_directories()

    if not skill_dirs:
        print("\n[!] No skills found in current directory!")
        print("    Make sure you're running this from the claude-skills-public directory.")
        return

    print(f"\nFound {len(skill_dirs)} skills:")
    for skill_dir in skill_dirs:
        print(f"  - {skill_dir.name}")

    # Install to Windows
    windows_installed = copy_skills_to_windows()

    # Install to WSL
    wsl_installed = copy_skills_to_wsl()

    # Summary
    print("\n" + "=" * 60)
    print("Installation Summary")
    print("=" * 60)
    print(f"[+] Windows: {len(windows_installed)} skills installed")
    if wsl_installed:
        print(f"[+] WSL: {len(wsl_installed)} skills installed")
    else:
        print(f"[!] WSL: Not installed (WSL not available or failed)")

    print("\n[*] Installation complete!")
    print("\nYou can now use these skills in Claude Code by invoking them.")
    print("Example: Ask Claude to 'use the refactoring-reviewer skill'")


if __name__ == "__main__":
    main()
