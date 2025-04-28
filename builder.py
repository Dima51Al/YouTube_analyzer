import PyInstaller.__main__
import shutil
import os
import sys

for folder in ['dist', 'build']:
    if os.path.exists(folder):
        shutil.rmtree(folder)
if os.path.exists('YouTube_analyzer.spec'):
    os.remove('YouTube_analyzer.spec')

main_script = os.path.abspath('app/main.py')

params = [
    main_script,
    '--onefile',
    '--noconsole',
    '--name=YouTube_analyzer',
    '--add-data=app/config.txt;.',
    '--hidden-import=requests',
    '--clean',
    '--paths=app',

]

try:
    PyInstaller.__main__.run(params)
except Exception as e:
    print(f"Ошибка при сборке: {e}")
    sys.exit(1)
