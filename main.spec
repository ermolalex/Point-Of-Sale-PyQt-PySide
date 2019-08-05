# -*- mode: python -*-

block_cipher = None


a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\lalan-ke\\Desktop\\MySale'],
             binaries=[],
             datas= [('msale/forms/*.ui', 'msale/forms' )],
             hiddenimports=["pytzdata"],
             hookspath=["pyinstaller_hooks"],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='msale',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,icon='icon.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='mysale')
