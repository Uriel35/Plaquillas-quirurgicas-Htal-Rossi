# -*- mode: python ; coding: utf-8 -*-
# main.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('credentials/email_credentials.json', 'credentials'),
    ],
    hiddenimports=[
        'numpy',
        'numpy.core',
        'numpy.lib',
        'pandas',
        'pandas._libs',
        'openpyxl',
        'googleapiclient',
        'google_auth_oauthlib',
        'google.auth',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    strip=False,
    upx=True,
    console=True,
)