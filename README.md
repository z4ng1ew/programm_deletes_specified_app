# Программа на Python для удаления приложений в Ubuntu

Ниже — безопасный скрипт с меню и подтверждением. Он делает всё то же, что мы делали руками: `apt purge`, `autoremove`, чистка конфигов и кеша.

## Вариант 1. Простой интерактивный скрипт

Сохрани как `uninstall_app.py`:

```python
#!/usr/bin/env python3
"""
uninstall_app.py — безопасное удаление приложения в Ubuntu/Debian.

Что делает:
  1. Проверяет, установлен ли пакет.
  2. Показывает, что именно будет удалено.
  3. Удаляет пакет (apt purge).
  4. Чистит зависимости (apt autoremove --purge).
  5. Опционально удаляет пользовательские конфиги/кеш.
  6. Опционально чистит кеш apt.

Запуск:
    sudo python3 uninstall_app.py
или (рекомендуется):
    sudo python3 uninstall_app.py <имя_пакета>
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
        result = subprocess.run(cmd, text=True, capture_output=True)
        if check and result.returncode != 0:
            print(result.stderr.strip())
            sys.exit(f"Ошибка выполнения: {' '.join(cmd)}")
        return result.stdout
    else:
        result = subprocess.run(cmd)
        if check and result.returncode != 0:
            sys.exit(f"Ошибка выполнения: {' '.join(cmd)}")
        return None


def require_root():
    if os.geteuid() != 0:
        sys.exit("Запусти от root: sudo python3 uninstall_app.py <пакет>")


def ask_yes_no(prompt, default=False):
    suffix = " [Y/n]: " if default else " [y/N]: "
    answer = input(prompt + suffix).strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes", "д", "да")


def is_installed(pkg: str) -> bool:
    result = subprocess.run(
        ["dpkg", "-s", pkg],
        text=True, capture_output=True
    )
    return result.returncode == 0


def get_home_of_user() -> Path:
    """Дом. каталог пользователя, который вызвал sudo."""
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return Path(f"/home/{sudo_user}")
    return Path.home()


# ---------------------- Основная логика ----------------------

def show_package_info(pkg: str):
    print(f"\n=== Информация о пакете '{pkg}' ===")
    info = run(
        ["apt-cache", "show", pkg],
        check=False, capture=True
    )
    if info:
        for line in info.splitlines():
            if line.startswith(("Package:", "Version:", "Description:", "Section:")):
                print("  " + line)

    print("\nЗависимости, которые могут стать ненужными:")
    run(["apt", "autoremove", "--dry-run", "--purge"], check=False)


def purge_package(pkg: str):
    print(f"\n=== Удаление пакета '{pkg}' (apt purge) ===")
    run(["apt", "purge", "-y", pkg])


def autoremove():
    print("\n=== Удаление ненужных зависимостей ===")
    run(["apt", "autoremove", "--purge", "-y"])


def clean_apt_cache():
    print("\n=== Чистка кеша apt ===")
    run(["apt", "clean"])
    run(["apt", "autoclean"])


def remove_user_files(pkg: str):
    """Удалить пользовательские конфиги и кеш с эвристикой по имени."""
    home = get_home_of_user()
    print(f"\n=== Удаление пользовательских файлов в {home} ===")

    candidates = [
        home / ".config" / pkg,
        home / ".cache" / pkg,
        home / ".local" / "share" / pkg,
    ]

    # Иногда имя каталога = имя пакета без префикса
    short = pkg.replace("-desktop", "").replace("-bin", "")
    if short != pkg:
        candidates += [
            home / ".config" / short,
            home / ".cache" / short,
            home / ".local" / "share" / short,
        ]

    found_any = False
    for path in candidates:
        if path.exists():
            found_any = True
            print(f"  Найдено: {path}")
            if ask_yes_no(f"    Удалить {path}?", default=False):
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)
                print("    Удалено.")
    if not found_any:
        print("  Ничего не найдено.")


def check_leftovers(pkg: str):
    print(f"\n=== Проверка остатков '{pkg}' ===")
    out = run(["dpkg", "-l", pkg], check=False, capture=True)
    if out and "ii" in out:
        print("  ⚠ Пакет всё ещё в списке установленных.")
    else:
        print("  ✅ Пакет удалён из dpkg.")

    which = shutil.which(pkg)
    if which:
        print(f"  ⚠ Найден бинарник в PATH: {which}")
    else:
        print("  ✅ Бинарник не найден в PATH.")


# ---------------------- Точка входа ----------------------

def main():
    require_root()

    if len(sys.argv) > 1:
        pkg = sys.argv[1].strip()
    else:
        pkg = input("Введи имя пакета для удаления (например sublime-text): ").strip()

    if not pkg:
        sys.exit("Имя пакета не задано.")

    if not is_installed(pkg):
        print(f"Пакет '{pkg}' не установлен (dpkg его не видит).")
        if not ask_yes_no("Всё равно попробовать удалить конфиги и кеш?"):
            sys.exit(0)
        remove_user_files(pkg)
        return

    show_package_info(pkg)

    print("\n⚠ Внимание: apt purge удалит пакет и его системные конфиги.")
    if not ask_yes_no(f"Продолжить удаление '{pkg}'?", default=False):
        sys.exit("Отменено пользователем.")

    purge_package(pkg)
    autoremove()

    if ask_yes_no("Удалить пользовательские конфиги и кеш?", default=True):
        remove_user_files(pkg)

    if ask_yes_no("Очистить кеш apt?", default=True):
        clean_apt_cache()

    check_leftovers(pkg)
    print("\n✅ Готово.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
        sys.exit(130)
```

## Как пользоваться

```bash
# сделать исполняемым
chmod +x uninstall_app.py

# удалить конкретный пакет
sudo python3 uninstall_app.py sublime-text

# или без аргумента — спросит имя
sudo python3 uninstall_app.py
```

Пример работы:

```
$ sudo python3 uninstall_app.py sublime-text

=== Информация о пакете 'sublime-text' ===
  Package: sublime-text
  Version: 4200
  ...
⚠ Внимание: apt purge удалит пакет и его системные конфиги.
Продолжить удаление 'sublime-text'? [y/N]: y
...
Удалить пользовательские конфиги и кеш? [Y/n]: y
Очистить кеш apt? [Y/n]: y
✅ Готово.
```

## Вариант 2. Минималистичный скрипт (без вопросов)

Если хочется одну команду без диалогов:

```python
#!/usr/bin/env python3
import os, sys, subprocess, shutil
from pathlib import Path

def run(*cmd):
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    if os.geteuid() != 0:
        sys.exit("Запусти с sudo")
    if len(sys.argv) < 2:
        sys.exit("Использование: sudo python3 uninstall.py <пакет>")

    pkg = sys.argv[1]
    home = Path(f"/home/{os.environ.get('SUDO_USER', 'root')}")

    run("apt", "purge", "-y", pkg)
    run("apt", "autoremove", "--purge", "-y")
    run("apt", "clean")

    for sub in ("config", "cache", "local/share"):
        path = home / "." / sub / pkg
        if path.exists():
            print("Удаляю:", path)
            shutil.rmtree(path, ignore_errors=True)

    print("Готово.")

if __name__ == "__main__":
    main()
```

Запуск:

```bash
sudo python3 uninstall.py sublime-text
```

## На что обратить внимание

1. **Скрипт требует root** — иначе apt не сможет удалять пакеты. Проверка `os.geteuid() != 0` это ловит.
2. **Пользовательские файлы** удаляются только с подтверждением (в первом варианте). Пути строятся по эвристике: `~/.config/<pkg>`, `~/.cache/<pkg>`, `~/.local/share/<pkg>`.
3. **`SUDO_USER`** используется, чтобы найти домашний каталог обычного пользователя, а не `/root`.
4. **`apt purge`** удаляет системные конфиги пакета, но **не** пользовательские — их чистит отдельная функция.
5. **Не запускай для критичных пакетов** (`systemd`, `apt`, `libc6` и т.п.) — можно сломать систему. Скрипт для обычных приложений вроде браузеров, редакторов, утилит.

Если хочешь, могу дописать:

- поддержку удаления **snap** и **flatpak** пакетов,
- поиск по части имени (`apt list --installed | grep ...`),
- логирование всех действий в файл,
- GUI на `tkinter`.
