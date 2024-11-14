import PyInstaller.__main__
import re
import datetime
import time
import os
import platform
import sys

# Read arguments from command line for platform-specific builds
platform_arg = sys.argv[1] if len(sys.argv) > 1 else None

# Check for Windows or GitHub Actions
isWindows = platform.system() == 'Windows'
isGithubActions = os.environ.get('CI', 'false') == 'true'

Version = "v0.1.1"
AppName = "DjangoRestfulAPI"
FileName = "DjangoRestfulAPI"
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
    kids=[StringFileInfo([
        StringTable('040904B0', [
            StringStruct('CompanyName', 'GuestLiang'),
            StringStruct('FileDescription', '{AppName} {Version}'),
            StringStruct('FileVersion', '{Version}'),
            StringStruct('InternalName', '{AppName}'),
            StringStruct('LegalCopyright', '2024 © GuestLiang'),
            StringStruct('OriginalFilename', '{AppName}.exe'),
            StringStruct('ProductName', 'GuestLiang Django Restful API'),
            StringStruct('ProductVersion', '{Version}')
        ])])],
    VarFileInfo([VarStruct('Translation', [2052, 1200])])]
)
'''

try:
    with open(VersionFileName, "w", encoding="utf-8") as f:
        f.write(VersionData)
except Exception as e:
    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Error writing file:', e)
    exit(0)

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Version file created successfully')
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Waiting for 5 seconds...')
time.sleep(5)

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] The version for this build is: {Version}')
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Running PyInstaller...')

# Build Python backend
Targets = []
if isGithubActions:
    print("[INFO] Running in GitHub Actions. Building for all platforms.")
    Targets = [
        {'platform': 'win32', 'distpath': 'dist/windows'},
        {'platform': 'linux', 'distpath': 'dist/linux'},
        {'platform': 'darwin', 'distpath': 'dist/macos_intel', 'arch': 'x86_64'},  # Intel (x64)
        {'platform': 'darwin', 'distpath': 'dist/macos_arm', 'arch': 'arm64'}     # ARM (Apple Silicon)
    ]
elif platform_arg == 'win':
    print("[INFO] Building for Windows only.")
    Targets = [{'platform': 'win32', 'distpath': 'dist/windows'}]
elif platform_arg == 'mac':
    print("[INFO] Building for macOS only.")
    Targets = [{'platform': 'darwin', 'distpath': 'dist/macos'}]
elif platform_arg == 'linux':
    print("[INFO] Building for Linux only.")
    Targets = [{'platform': 'linux', 'distpath': 'dist/linux'}]
else:
    print("[INFO] Invalid platform specified. Exiting...")
    exit(1)

for Target in Targets:
    args = [
        'manage.py',
        f'--name={FileName}',
        '--onefile',  # Single executable file
        '--console',  # Console output
        '--hidden-import=django.contrib.admin',
        '--hidden-import=django.contrib.auth',
        '--hidden-import=django.contrib.contenttypes',
        '--hidden-import=django.contrib.sessions',
        '--hidden-import=django.contrib.messages',
        '--hidden-import=django.contrib.staticfiles',
        '--hidden-import=rest_framework',
        '--hidden-import=api',
        '--hidden-import=corsheaders',
        '--add-data=storage:storage',
        '--add-data=transit:transit',
        '--add-data=pic:pic',
        f'--version-file={VersionFileName}',
        '--distpath', Target['distpath'],
        '--workpath', 'build',
    ]

    if Target['platform'] == 'win32':
        args.append('--platform=win32')
    elif Target['platform'] == 'linux':
        args.append('--platform=linux')
    elif Target['platform'] == 'darwin':
        args.append('--platform=darwin')
        if 'arch' in Target:
            args.append(f'--arch={Target["arch"]}')

    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Building for platform: {Target["platform"]} with arch: {Target.get("arch", "default")}')
    PyInstaller.__main__.run(args)

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] PyInstaller finished, cleaning spec file...')
os.remove(f"{FileName}.spec")
