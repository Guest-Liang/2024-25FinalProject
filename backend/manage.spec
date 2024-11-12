# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('storage', 'storage'),
        ('transit', 'transit'),
        ('pic', 'pic'),
    ],
    hiddenimports=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        'rest_framework',
        'api',
        'corsheaders',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DjangoRestfulAPI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    company_name='GuestLiang',
    product_name='GuestLiang Django Restful API',
    product_version='1.0.0rc1',
    file_description='DjangoRestfulAPI, works on Port 8000',
    copyright='© 2024 GuestLiang',
)
