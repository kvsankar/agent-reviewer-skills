#!/usr/bin/env python3
"""
Install Claude Code skills to both Windows and WSL ~/.claude/skills/ directories.

This script works from both Windows and WSL environments:
- From WSL: Installs to WSL ~/.claude/skills/ and Windows /mnt/c/Users/<user>/.claude/skills/
- From Windows: Installs to Windows ~/.claude/skills/ and WSL via wsl.exe
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def is_running_in_wsl() -> bool:
    """Detect if we're running inside WSL."""
    try:
        with open("/proc/version") as f:
            content = f.read().lower()
            return "microsoft" in content or "wsl" in content
    except OSError:
        return False


def get_skill_directories():
    """Find all skill directories (containing SKILL.md) in the current directory."""
    current_dir = Path(__file__).parent
    skill_dirs = []

    for item in current_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skill_dirs.append(item)

    return skill_dirs


def copy_skills_to_directory(target_dir: Path, label: str):
    """Copy skills to a target directory.

    Args:
        target_dir: Target directory path
        label: Label for display (e.g., 'WSL', 'Windows')

    Returns:
        List of installed skill names
    """
    print(f"\n[*] Installing skills to {label}: {target_dir}")
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


def get_windows_home_from_wsl(username: str = None) -> Path:
    """
    Get Windows user home directory from WSL.

    Args:
        username: Optional Windows username. If None, uses USERPROFILE.

    Returns:
        Path to Windows home directory, or None if not found.
    """
    # Primary approach: use Windows USERPROFILE via cmd.exe
    try:
        result = subprocess.run(
            ["cmd.exe", "/c", "echo %USERPROFILE%"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        win_path = result.stdout.strip()
        if win_path and win_path != "%USERPROFILE%":
            result = subprocess.run(
                ["wslpath", win_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            wsl_path = Path(result.stdout.strip())
            if wsl_path.exists():
                return wsl_path
    except (subprocess.SubprocessError, subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    # Fallback: scan /mnt drives for Claude installation
    mnt = Path("/mnt")
    if not mnt.exists():
        return None

    for drive in sorted(mnt.iterdir()):
        if not (drive.is_dir() and len(drive.name) == 1 and drive.name.isalpha()):
            continue
        users_dir = drive / "Users"
        if not users_dir.exists():
            continue
        for user_dir in users_dir.iterdir():
            if user_dir.is_dir() and not user_dir.is_symlink():
                # Check if .claude directory exists (even without skills yet)
                if (user_dir / ".claude").exists():
                    return user_dir

    return None


def install_from_wsl():
    """Install skills when running from WSL."""
    results = {}

    # Install to WSL (local)
    wsl_target = Path.home() / ".claude" / "skills"
    wsl_installed = copy_skills_to_directory(wsl_target, "WSL")
    results["WSL"] = wsl_installed

    # Install to Windows
    windows_home = get_windows_home_from_wsl()
    if windows_home:
        windows_target = windows_home / ".claude" / "skills"
        windows_installed = copy_skills_to_directory(windows_target, "Windows")
        results["Windows"] = windows_installed
    else:
        print("\n[!] Windows: Could not find Windows home directory")
        print("    Ensure Claude Code is installed on Windows and .claude directory exists")
        results["Windows"] = None

    return results


def install_from_windows():
    """Install skills when running from native Windows."""
    results = {}

    # Install to Windows (local)
    windows_target = Path.home() / ".claude" / "skills"
    windows_installed = copy_skills_to_directory(windows_target, "Windows")
    results["Windows"] = windows_installed

    # Install to WSL
    try:
        # Get WSL username
        result = subprocess.run(
            ["wsl", "echo", "$USER"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            print("\n[!] WSL: Not available or not configured")
            results["WSL"] = None
            return results

        wsl_user = result.stdout.strip()
        wsl_home = f"/home/{wsl_user}"
        wsl_target = f"{wsl_home}/.claude/skills"

        print(f"\n[*] Installing skills to WSL: {wsl_target}")

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

        results["WSL"] = installed

    except subprocess.TimeoutExpired:
        print("\n[!] WSL: Command timed out")
        results["WSL"] = None
    except FileNotFoundError:
        print("\n[!] WSL: Not found (wsl.exe not in PATH)")
        results["WSL"] = None
    except Exception as e:
        print(f"\n[!] WSL: Error - {e}")
        results["WSL"] = None

    return results


def main():
    print("=" * 60)
    print("Claude Code Skills Installer")
    print("=" * 60)

    # Detect environment
    in_wsl = is_running_in_wsl()
    env_name = "WSL" if in_wsl else "Windows"
    print(f"\nRunning from: {env_name}")

    skill_dirs = get_skill_directories()

    if not skill_dirs:
        print("\n[!] No skills found in current directory!")
        print("    Make sure you're running this from the claude-skills directory.")
        return

    print(f"\nFound {len(skill_dirs)} skills:")
    for skill_dir in skill_dirs:
        print(f"  - {skill_dir.name}")

    # Install based on environment
    if in_wsl:
        results = install_from_wsl()
    else:
        results = install_from_windows()

    # Summary
    print("\n" + "=" * 60)
    print("Installation Summary")
    print("=" * 60)

    for env, installed in results.items():
        if installed is not None:
            print(f"[+] {env}: {len(installed)} skills installed")
        else:
            print(f"[!] {env}: Not installed (not available or failed)")

    print("\n[*] Installation complete!")
    print("\nYou can now use these skills in Claude Code by invoking them.")
    print("Example: Ask Claude to 'use the refactoring-reviewer skill'")


if __name__ == "__main__":
    main()
