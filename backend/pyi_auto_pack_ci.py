import PyInstaller.__main__
import re, datetime, time, os, sys
from Configs import CONFIG

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
from django.conf import settings
settings.configure()

# Read arguments from command line for platform-specific builds
PlatformArg = sys.argv[1] if len(sys.argv) > 1 else None

# Check for GitHub Actions
isGithubActions = os.environ.get('CI', 'false') == 'true'

# Basic app info
VersionFileName = "version_autogen.txt"

# Parse version number
match = re.match(r"v(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?", CONFIG['API']['Version'])
if match:
    major, minor, patch, build = match.groups()
    build = build if build is not None else "0"
else:
    raise ValueError("Invalid version format")

# Version data to include in the build
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
                        StringStruct('CompanyName', '{CONFIG['API']['CompanyName']}'),
                        StringStruct('FileDescription', '{CONFIG['API']['AppName']} {CONFIG['API']['Version']}'),
                        StringStruct('FileVersion', '{CONFIG['API']['Version']}'),
                        StringStruct('InternalName', '{CONFIG['API']['AppName']}'),
                        StringStruct('LegalCopyright', '{CONFIG['API']['LegalCopyright']}'),
                        StringStruct('OriginalFilename', '{CONFIG['API']['AppName']}.exe'),
                        StringStruct('ProductName', '{CONFIG['API']['ProductName']}'),
                        StringStruct('ProductVersion', '{CONFIG['API']['Version']}')
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct('Translation', [2052, 1200])])
    ]
)
'''

# Write version data to a file
try:
    with open(VersionFileName, "w", encoding="utf-8") as f:
        f.write(VersionData)
except Exception as e:
    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Error writing file:', e)
    exit(0)

# Log version creation
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Version file created successfully')
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Waiting for 1 seconds...')
time.sleep(1)

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] The version for this build is: {CONFIG['API']['Version']}')
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Running PyInstaller...')

# Define platform-specific configurations in a dictionary
Platforms = {
    'win': {'distpath': 'dist/windows', 'platform': 'win32'},
    'linux': {'distpath': 'dist/linux', 'platform': 'linux'}
}

# Check platform argument and construct the necessary build arguments
if PlatformArg in Platforms:
    print(f"[INFO] Building for {PlatformArg.capitalize()}.")
    config = Platforms[PlatformArg]

    # Build arguments for PyInstaller
    args = [
        'manage.py',
        f'--name={CONFIG['API']['FileName']}',
        '--onefile',            # Single executable file
        '--console',            # Console output
        '--noconfirm',          # Automatic confirmation, ignore all prompts
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
        '--distpath', config['distpath'],
        '--workpath', 'build',
    ]

    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Building for platform: {PlatformArg}')
    PyInstaller.__main__.run(args)
else:
    print(f"[INFO] Invalid platform specified: {PlatformArg}. Exiting...")
    exit(1)

# Clean up spec file
print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] PyInstaller finished, cleaning spec file...')
os.remove(f"{CONFIG['API']['FileName']}.spec")

print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] All done, exiting...')
