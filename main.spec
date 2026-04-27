# -*- mode: python ; coding: utf-8 -*-
# main.spec
block_cipher = None
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect everything needed for pandas/numpy (code, binaries, datas, hidden imports).
# Esto hace el build más pesado pero mucho más robusto en Windows.
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[] + numpy_binaries + pandas_binaries,
    datas=[
        ('credentials/email_credentials.json', 'credentials'),
        ('data/htal_rossi_logo.png', 'data'),
    ] + numpy_datas + pandas_datas,
    hiddenimports=[
        # Aseguramos raíz de paquetes aunque el import sea "diferido" (dentro de funciones).
        'numpy',
        'pandas',
        'openpyxl',
        'googleapiclient',
        'google_auth_oauthlib',
        'google.auth',
    ]
    + numpy_hiddenimports
    + pandas_hiddenimports
    # Belt-and-suspenders: algunos entornos/versions no resuelven bien todos los imports dinámicos de pandas/numpy.
    + collect_submodules('numpy')
    + collect_submodules('pandas'),
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
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    strip=False,
    upx=False,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='main',
)
