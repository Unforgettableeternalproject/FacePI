# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

SETUP_DIR = 'C:\\Users\wishingsoft\Documents\FacePI'

a = Analysis(['ControlPanel.py', 'C:\\Users\\wishingsoft\\Documents\\FacePI\\IncludedClasses\\MainProgram.py','C:\\Users\\wishingsoft\\Documents\\FacePI\\IncludedClasses\\ClassWindow.py','C:\\Users\\wishingsoft\\Documents\\FacePI\\IncludedClasses\\ClassPersonGroup.py','C:\\Users\\wishingsoft\\Documents\\FacePI\\IncludedClasses\\ClassPerson.py','C:\\Users\\wishingsoft\\Documents\\FacePI\\IncludedClasses\\ClassOpenCV.py','C:\\Users\\wishingsoft\\Documents\\FacePI\\IncludedClasses\\ClassFacePI.py','C:\\Users\\wishingsoft\\Documents\\FacePI\\IncludedClasses\\ClassConfig.py'],
             pathex=[],
             binaries=[],
             datas=[(SETUP_DIR+'\\IncludedClasses\\*', '.')],
             hiddenimports=['IncludedClasses.MainProgram', '.ClassWindow', '.ClassPersonGroup', '.ClassPerson', '.ClassOpenCV', '.ClassFacePI', '.ClassConfig', 'cython', 'sklearn', 'sklearn.ensemble', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils', 'sklearn.utils._cython_blas'],
             hookspath=[],
             hooksconfig={},
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
          name='FacePI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ControlPanel')
