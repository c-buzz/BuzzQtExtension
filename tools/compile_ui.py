from pathlib import Path
import multiprocessing as mp
import subprocess

# Compatibility with Python < 3.9
import sys
if sys.version_info.minor < 9:
    def _with_stem(self: Path, stem: str):
        # Get current stem
        _stem = self.stem
        _ext = self.suffix
        _parent = self.parent
        return (_parent / stem).with_suffix(_ext)
    Path.with_stem = _with_stem


# Find correct qt version used
uic_commands = dict(pyside2="pyside2-uic", pyside6="pyside6-uic", pyqt5="pyuic5", pyqt6="pyuic6")
rcc_commands = dict(pyside2="pyside2-rcc", pyside6="pyside6-rcc", pyqt5="pyuic5", pyqt6="pyuic6")

def search_qt_api() ->str:
    import os
    qt_api = None
    if 'QT_API' in os.environ and (os.environ['QT_API'] in uic_commands.keys()):
        qt_api = os.environ['QT_API']
    else:
        try:
            import qtpy
        except:
            import importlib
            for ver in ["PySide2", "PySide6", "PyQt5", "PyQt6"]:
                try:
                    importlib.import_module(ver)
                except:
                    pass
                else:
                    qt_api = ver
                    break
        else:
            qt_api = qtpy.API
    if qt_api is None:
        raise "No Qt module found in this environment. Please install any [PySide2, PySide6, PyQt5, PyQt6]"
    return qt_api

qt_api = search_qt_api()
uic_command = uic_commands[qt_api]
rcc_command = rcc_commands[qt_api]

def _pool_compiler_subprocess(cmd):
    subprocess.run(cmd)


def compile_ui(*_dirs, resources=True, recursive=True):
    commands = []

    for _dir in _dirs:
        _dir = Path(_dir).resolve()

        glob = _dir.rglob if recursive else _dir.glob

        for ui in glob('*.ui'):
            fn = ui.stem

            # Underscore to CamelCase
            # cc_name = ''.join(x.capitalize() or '_' for x in fn.split('_')) + 'Ui.py'
            # fn = _dir / cc_name

            command = f"{uic_command} {ui} -o {ui.with_suffix('.py').with_stem(ui.stem + 'Ui')} --from-imports"
            commands.append(command)

        if not resources:
            continue

        for res in _dir.glob('*.qrc'):
            fn = _dir / (res.stem + '_rc.py')
            command = f'{rcc_command} {res} -o {fn}'
            commands.append(command)

    pool = mp.Pool()
    pool.map(_pool_compiler_subprocess, commands)
    pool.close()
    pool.terminate()
    print(f'Converted ui files in directory {_dir}')

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    compile_ui(*args)
