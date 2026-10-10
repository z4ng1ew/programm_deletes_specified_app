#!/usr/bin/env python3
"""
uninstall_app.py — безопасное удаление приложения.
Поддержка: Ubuntu/Debian (apt/dpkg) и Fedora/RHEL (dnf/rpm).

Использование:
    sudo python3 uninstall_app.py <имя_пакета>
    sudo ./uninstall_app.py <имя_пакета>
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


# ---------------------- Утилиты ----------------------

def run(cmd, check=True, capture=False):
    """Запустить команду. По умолчанию выводит в терминал."""
    print(f"\n$ {' '.join(cmd)}")
    if capture:
        r = subprocess.run(cmd, text=True, capture_output=True)
        if check and r.returncode != 0:
            print(r.stderr.strip())
            sys.exit(f"Ошибка: {' '.join(cmd)}")
        return r.stdout
    r = subprocess.run(cmd)
    if check and r.returncode != 0:
        sys.exit(f"Ошибка: {' '.join(cmd)}")
    return None


def require_root():
    if os.geteuid() != 0:
        sys.exit("Запусти от root: sudo ./uninstall_app.py <пакет>")


def ask_yes_no(prompt, default=False):
    suffix = " [Y/n]: " if default else " [y/N]: "
    a = input(prompt + suffix).strip().lower()
    return default if not a else a in ("y", "yes", "д", "да")


def get_user_home() -> Path:
    """Домашний каталог пользователя, вызвавшего sudo."""
    u = os.environ.get("SUDO_USER")
    return Path(f"/home/{u}") if u else Path.home()


# ---------------------- Бэкенды пакетных менеджеров ----------------------

class AptBackend:
    """Ubuntu / Debian / Mint."""
    name = "apt / dpkg"

    def is_installed(self, pkg):
        return subprocess.run(
            ["dpkg", "-s", pkg], capture_output=True
        ).returncode == 0

    def info(self, pkg):
        out = run(["apt-cache", "show", pkg], check=False, capture=True)
        if out:
            for line in out.splitlines():
                if line.startswith(("Package:", "Version:", "Description:", "Section:")):
                    print("  " + line)
        print("\nЗависимости, которые могут стать ненужными:")
        run(["apt", "autoremove", "--dry-run", "--purge"], check=False)

    def purge(self, pkg):
        run(["apt", "purge", "-y", pkg])

    def autoremove(self):
        run(["apt", "autoremove", "--purge", "-y"])

    def clean(self):
        run(["apt", "clean"])
        run(["apt", "autoclean"])

    def leftover(self, pkg):
        out = run(["dpkg", "-l", pkg], check=False, capture=True)
        if out and any(l.startswith("ii") for l in out.splitlines()):
            print("  ⚠ Пакет всё ещё в dpkg.")
        else:
            print("  ✅ Пакет удалён из dpkg.")


class DnfBackend:
    """Fedora / RHEL / CentOS / Rocky / AlmaLinux."""
    name = "dnf / rpm"

    def is_installed(self, pkg):
        return subprocess.run(
            ["rpm", "-q", pkg], capture_output=True
        ).returncode == 0

    def info(self, pkg):
        out = run(["dnf", "info", pkg], check=False, capture=True)
        if out:
            for line in out.splitlines():
                if line.startswith(("Name", "Version", "Release", "Summary", "Size")):
                    print("  " + line)

    def purge(self, pkg):
        # dnf remove удаляет пакет и его файлы
        run(["dnf", "remove", "-y", pkg])
        # подчистим системные конфиги, если остались (аналог apt purge)
        etc_dir = Path("/etc") / pkg
        if etc_dir.exists() and etc_dir.is_dir():
            print(f"\nНайден /etc/{pkg}, удаляю…")
            shutil.rmtree(etc_dir, ignore_errors=True)

    def autoremove(self):
        run(["dnf", "autoremove", "-y"])

    def clean(self):
        run(["dnf", "clean", "all"])

    def leftover(self, pkg):
        r = subprocess.run(["rpm", "-q", pkg], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  ⚠ Пакет всё ещё установлен: {r.stdout.strip()}")
        else:
            print("  ✅ Пакет удалён из rpm.")


def detect_backend():
    if shutil.which("apt") and shutil.which("dpkg"):
        return AptBackend()
    if shutil.which("dnf") and shutil.which("rpm"):
        return DnfBackend()
    sys.exit("Не найден поддерживаемый пакетный менеджер (apt/dpkg или dnf/rpm).")


# ---------------------- Пользовательские файлы ----------------------

def remove_user_files(pkg):
    home = get_user_home()
    print(f"\n=== Пользовательские файлы в {home} ===")

    candidates = [
        home / ".config" / pkg,
        home / ".cache" / pkg,
        home / ".local" / "share" / pkg,
    ]
    short = pkg.replace("-desktop", "").replace("-bin", "")
    if short != pkg:
        candidates += [
            home / ".config" / short,
            home / ".cache" / short,
            home / ".local" / "share" / short,
        ]

    found = False
    for p in candidates:
        if p.exists():
            found = True
            print(f"  Найдено: {p}")
            if ask_yes_no(f"    Удалить {p}?", default=False):
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink(missing_ok=True)
                print("    Удалено.")
    if not found:
        print("  Ничего не найдено.")


# ---------------------- main ----------------------

def main():
    require_root()
    backend = detect_backend()
    print(f"Пакетный менеджер: {backend.name}")

    if len(sys.argv) > 1:
        pkg = sys.argv[1].strip()
    else:
        pkg = input("Имя пакета для удаления: ").strip()

    if not pkg:
        sys.exit("Имя пакета не задано.")

    if not backend.is_installed(pkg):
        print(f"\nПакет '{pkg}' не найден в системе.")
        if not ask_yes_no("Всё равно удалить конфиги и кеш?"):
            sys.exit(0)
        remove_user_files(pkg)
        return

    print(f"\n=== Информация о '{pkg}' ===")
    backend.info(pkg)

    print(f"\n⚠ Будет удалён пакет '{pkg}' и его системные конфиги.")
    if not ask_yes_no("Продолжить?", default=False):
        sys.exit("Отменено.")

    backend.purge(pkg)
    backend.autoremove()

    if ask_yes_no("Удалить пользовательские конфиги и кеш?", default=True):
        remove_user_files(pkg)

    if ask_yes_no("Очистить кеш пакетного менеджера?", default=True):
        backend.clean()

    print("\n=== Проверка остатков ===")
    backend.leftover(pkg)
    print("\n✅ Готово.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано.")
        sys.exit(130)
