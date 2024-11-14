import PyInstaller.__main__
import re
import datetime
import time
import os

Version = "v0.1.1"
AppName = "DjangoRestfulAPI"
FileName = f"distribution-{Version}-DjangoRestfulAPI"
VersionFileName = "version_autogen.txt"

match = re.match(r"v(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?", Version)

if match:
    major, minor, patch, build = match.groups()
    build = build if build is not None else "0"  # build defaults to 0
else:
    raise ValueError("Invalid version format")

VersionData = f'''
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({major}, {minor}, {patch}, {build}),
        prodvers=({major}, {minor}, {patch}, {build}),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'GuestLiang'),
                        StringStruct('FileDescription', '{AppName} works on Port 8000'),
                        StringStruct('FileVersion', '{Version}'),
                        StringStruct('InternalName', '{AppName}'),
                        StringStruct('LegalCopyright', '2024 © GuestLiang'),
                        StringStruct('OriginalFilename', '{AppName}.exe'),
                        StringStruct('ProductName', 'GuestLiang Django Restful API'),
                        StringStruct('ProductVersion', '{Version}')
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct('Translation', [2052, 1200])])
    ]
)
'''

try:
    with open(VersionFileName, "w", encoding="utf-8") as f:
        f.write(VersionData)
except Exception as e:
    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Error writing file:', e)
    exit(0)

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Version file created successfully')
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Wating for 5 seconds...')
time.sleep(5)

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] The version for this build is: {Version}')
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Running PyInstaller...')

PyInstaller.__main__.run([
    'manage.py',
    f'--name={FileName}',
    '--onefile',
    '--console',
    '--hidden-import=django.contrib.admin',
    '--hidden-import=django.contrib.auth',
    '--hidden-import=django.contrib.contenttypes',
    '--hidden-import=django.contrib.sessions',
    '--hidden-import=django.contrib.messages',
    '--hidden-import=django.contrib.staticfiles',
    '--hidden-import=rest_framework',
    '--hidden-import=api',
    '--hidden-import=corsheaders',
    '--add-data=storage;storage',
    '--add-data=transit;transit',
    '--add-data=pic;pic',
    f'--version-file={VersionFileName}',
    '--distpath', 'dist',
    '--workpath', 'build',
])

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] PyInstaller finished, cleaning spec file...')
os.remove(f"{FileName}.spec")
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] All done, exiting...')