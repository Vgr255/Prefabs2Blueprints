## Prefabs2Blueprints Version 0.4

This Python script converts Space Engineers prefabs to Blueprints.

To use P2B, you need [Python][0]. Either Python 2 or 3 will work.

### Requirements

To use the script, you need to either download and install [Git][1] and then [clone the repository][2], or [download the code directly][3].

If you're confused, [just download and install Python][0] and [download the code][3].

### Using the code

Single file:

1. Browse to `C:/Users/<YourName>/AppData/Roaming/SpaceEngineers/Blueprints/local`.
2. Create a new folder in there. Name it however you like.
3. Put in that folder the `.sbc` prefab file you want to convert.
4. Browse where you downloaded the code.
5. Copy or rename `config.py.example` to `config.py`.
6. Open `config.py` with any text editor.
7. Edit `NAME` to the name of the folder you created in step 2.
8. You may edit any other setting to your liking.

Multiple files:

1. Create a new folder anywhere you like.
2. Put all the `.sbc` prefabs that you want to convert in that folder.
3. Browse where you downloaded the code.
4. Copy or rename `config.py.example` to `config.py`.
5. Open `config.py` with any text editor.
6. Edit `BATCH_PATH` to the full path of the folder you created in step 1.
7. Use only forward slashes `/` or double-backward slashes `\\` in the path.
8. The name of the `.sbc` files will be the folders' names.
9. You can add something to `APPEND` and `PREPEND`, P2B will respectively append or prepend those to the path.

When you're done editing your settings, save `config.py` and double-click on `converter.py`.
Wait a bit and it should complete without problem.

Please report any issue using the [GitHub issue tracker][4].

Changelog:

0.1 - First version

0.2 - Batch mode, pretty much final release

0.3 - Backwards compatibility

0.4 - Add proper UTF-8 handling, and properly handle nonsense

[0]: https://www.python.org/ftp/python/3.5.0/python-3.5.0.exe
[1]: http://git-scm.com/download/win
[2]: github-windows://openRepo/https://github.com/Vgr255/Prefabs2Blueprints
[3]: https://github.com/Vgr255/Prefabs2Blueprints/archive/master.zip
[4]: https://github.com/Vgr255/Prefabs2Blueprints/issues
