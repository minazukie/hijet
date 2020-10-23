import argparse
import os
import pathlib
import subprocess

DEFAULT_IDE = "intellij idea"


def generate_ide_map():
    ides = {
        "pycharm": ("py", "pyc"),
        "webstorm": ("js", "css", "html", "less", "sass", "scss"),
        "goland": ("go",),
        "rubymine": ("rb",),
        "clion": ("c", "h", "cc", "cpp", "hpp", "rs"),
        "phpstorm": ("php",),
        "appcode": ("swift", "m"),
        "rider": ("cs",),
        DEFAULT_IDE: ("java", "kotlin"),
    }
    _map = {}
    for _ide, _exts in ides.items():
        for e in _exts:
            _map[e] = _ide
    return _map


ide_map = generate_ide_map()
exclude_dirs = ["node_modules", "venv"]
stat = {}


def count_files(files):
    for f in files:
        ext = pathlib.Path(f).suffix[1:]
        if ext in stat:
            stat[ext] += 1
        else:
            stat[ext] = 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", action="append", default=[])
    parser.add_argument("-d", default=pathlib.Path.cwd())
    args = parser.parse_args()

    exclude_dirs.extend(args.e)
    path = args.d

    for root, dirs, files in os.walk(path):
        parts = pathlib.Path(root).relative_to(pathlib.Path(path)).parts
        if parts == ():
            count_files(files)
            continue
        if parts and parts[0] and parts[0][0] != "." and parts[0] not in exclude_dirs:
            count_files(files)

    if not stat:
        print("no files or directories here.")
        return

    ide_name = DEFAULT_IDE

    sorted_stat = sorted(stat.items(), key=lambda x: x[1])

    while sorted_stat:
        ext = sorted_stat.pop()[0]
        if ext in ide_map:
            ide_name = ide_map[ext]
            break

    if "sln" in stat:
        ide_name = "rider"

    print(f"opening {ide_name}...")
    subprocess.run(f'open -a "{ide_name}" {path}', shell=True)


if __name__ == "__main__":
    main()
