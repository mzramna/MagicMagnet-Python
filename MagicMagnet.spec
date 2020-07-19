# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['MagicMagnet.py'],
             pathex=['C:\\Users\\migue\\Documents\\MagicMagnet-Python'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('icon.png','C:\\Users\\migue\\Documents\\MagicMagnet-Python\\icon.png', "DATA")]
a.datas += [('search_parameters.json','C:\\Users\\migue\\Documents\\MagicMagnet-Python\\search_parameters.json', "DATA")]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MagicMagnet',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
