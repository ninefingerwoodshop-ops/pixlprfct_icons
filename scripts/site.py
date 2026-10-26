import json, shutil, zipfile
from pathlib import Path
root=Path(__file__).resolve().parent.parent
out=root/'_site'
if out.exists(): shutil.rmtree(out)
shutil.copytree(root/'site',out)
for directory in ['fonts','css']: shutil.copytree(root/directory,out/directory)
shutil.copy(root/'icons.json',out/'icons.json')
(out/'downloads').mkdir()
with zipfile.ZipFile(out/'downloads/pixlprfct-icons.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for name in ['fonts','css','icons.json','README.md','LICENSE']:
        path=root/name
        for file in sorted(path.rglob('*')) if path.is_dir() else [path]:
            if file.is_file(): archive.write(file,Path('pixlprfct-icons')/file.relative_to(root))
print('Built gallery and downloadable font package in _site/')
