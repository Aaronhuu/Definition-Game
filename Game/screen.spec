# -*- mode: python -*-

import sys


a = Analysis(['screen.py'],
             pathex=['/Users/aaronhu/Documents/workspace/difinitives'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,

          a.binaries + [('msvpc100.dll','c:\\Windows\\System32\\msvpc100.dll','BINARY'),
                        ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll','BINARY')]
          if sys.platform == 'win32' else a.binaries,
          a.zipfiles,
          a.datas + [('data/bg1.jpg',    '/Users/aaronhu/Documents/workspace/difinitives/data/bg1.jpg','DATA' ),
                    ('data/bg2.jpg',    '/Users/aaronhu/Documents/workspace/difinitives/data/bg2.jpg','DATA'),
                    ('data/bg3.jpg',    '/Users/aaronhu/Documents/workspace/difinitives/data/bg3.jpg','DATA'),
                    ('data/blurbg.jpg',    '/Users/aaronhu/Documents/workspace/difinitives/data/blurbg.jpg','DATA'),
                    ('data/database.xls',    '/Users/aaronhu/Documents/workspace/difinitives/data/database.xls','DATA'),
                    ('data/leftwing.png',    '/Users/aaronhu/Documents/workspace/difinitives/data/leftwing.png','DATA'),
                    ('data/pygame_logo.png',    '/Users/aaronhu/Documents/workspace/difinitives/data/Python.png','DATA'),
                    ('data/Python.png',    '/Users/aaronhu/Documents/workspace/difinitives/data/Python.png','DATA'),       
                    ('data/rightwing.png',    '/Users/aaronhu/Documents/workspace/difinitives/data/rightwing.png','DATA'),
                    ('data/back.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/back.ttf','DATA'),
                    ('data/choose.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/choose.ttf','DATA'),
                    ('data/f1.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/f1.ttf','DATA'),
                    ('data/flaticon.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/flaticon.ttf','DATA'),
                    ('data/flaticon2.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/flaticon2.ttf','DATA'),
                    ('data/flaticon3.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/flaticon3.ttf','DATA'),
                    ('data/home.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/home.ttf','DATA'),
                    ('data/load.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/load.ttf','DATA'),
                    ('data/pause.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/pause.ttf','DATA'),
                    ('data/people.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/people.ttf','DATA'),
                    ('data/Roboto-Bold.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/Roboto-Bold.ttf','DATA'),
                    ('data/Roboto-Light.ttf',    '/Users/aaronhu/Documents/workspace/difinitives/data/Roboto-Light.ttf','DATA'),
                    ('data/click.wav',    '/Users/aaronhu/Documents/workspace/difinitives/data/click.wav','DATA'),
                    ('data/space.jpg',    '/Users/aaronhu/Documents/workspace/difinitives/data/space.jpg','DATA')
                    ],
          name = os.path.join('dist', 'screen' + ('.exe' if sys.platform == 'win32' else '')),
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon ='difinitives/data/icon.png' )

if sys.platform == 'darwin':
	app = BUNDLE(exe,
		name = 'screen.app',
		icon=None
		)

# coll = COLLECT(exe,
#                a.binaries,
#                a.zipfiles,
#                a.datas,
#                strip=None,
#                upx=True,
#                name='screen')
