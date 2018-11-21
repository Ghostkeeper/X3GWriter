# X3GWriter
X3G output plugin for Cura. This allows saving the slice output as an X3G file for printers based on the Sailfish firmware.

This plug-in takes the normal g-code output of Cura, and converts it using [GPX](https://github.com/Ghostkeeper/GPX) to the X3G format.

## Support
X3GWriter supports Windows, MacOS and Linux.

X3GWriter supports all parameters of GPX to convert g-code to X3G. Our version of GPX has profiles for the following printers:
* Cupcake Gen3 XYZ
* Cupcake Gen4 XYZ
* Cupcake Pololu XYZ
* Core-XY with heated build plate, single extruder
* Clone R1
* Replicator 1
* Replicator 2
* Replicator 2X
* TOM Mk6
* TOM Mk7
* ZYYX
* FlashForge Creator Pro

If your printer is not in there, it can still be defined (using Cura's *.def.json files) with custom parameters.

## Installation
There are multiple ways in which you could install this plug-in.

### Via the Toolbox in Cura
1. Open Cura.
2. In the application menu, go to Toolbox -> Browse Packages.
3. Under the Plugins tab, find X3GWriter. Click the Install button to install it there.
4. Restart Cura.

### Via the Curaplugin file
1. Download the .curaplugin file of the latest release from Github: https://github.com/Ghostkeeper/X3GWriter/releases/latest
2. Drag the .curaplugin file onto the Cura window.
3. Restart Cura.

### Using the source code
1. Download the .zip file from Github: https://github.com/Ghostkeeper/X3GWriter/archive/master.zip
2. Open the .zip file with your favourite archiver application (e.g. 7-zip).
3. Open Cura and in the application menu go to Help -> Show Configuration Folder.
4. In the configuration folder, go the subfolder for your current Cura version and then the `/plugins` subfolder.
5. Extract the contents of the .zip archive to that subfolder. Make sure that there is now a file called `.../plugins/X3GWriter/__init__.py`
6. Restart Cura.

## Usage
Once installed, you should now be able to select X3G output for printers that support it. Try the Malyan M180 printer. Load a mesh, and save the output to a file. In the file dialogue, you should now be able to select the X3G format.

## Compiling
X3GWriter is compiled using CMake. Basically what this does is to compile its dependecy, GPX, and places it in the correct location when you install or package.

Compiling is done using the standard CMake workflow, namely:

1. (Recommended) Create a directory to build in, with the command `mkdir build`, then `cd build`.
2. Configure and generate with CMake with the command `cmake ..`.
3. If desired, change the install directory. For instance:
   1. Find the plugins directory of Cura, such as `C:\Users\<You>\AppData\Roaming\cura\2.7\plugins` on Windows, `~/.local/cura/2.7/plugins` on Linux or `/Library/Application Support/cura/2.7/plugins` on MacOS.
   2. Open CMake configuration using `cmake-gui .` or `ccmake .`.
   3. Toggle the advanced options. In CMake-GUI this is done with a checkbox at the top. In ccmake this is with the `t` key.
   4. Change the variable `CMAKE_INSTALL_PREFIX` to the installation directory found at step 3.1.
4. Configure. In CMake-GUI this is done with the "Configure" button. In ccmake this is done with the `c` key.
   1. If there were any errors, this is likely when you need to resolve them. In particular, please check whether the X3G executable was found. If it wasn't found, you will need to point CMake to the location of your GPX executable (likely in your Program Files or /usr/local somewhere).
5. Generate. In CMake-GUI this is done with the "Generate" button. In ccmake this is done with the `g` key.
6. Compile. This depends on your compiler. With GCC this is the `make` command. With MinGW this is the `mingw32-make` command. With MSVC this is with the `nmake` command.
7. Install with the command `make install` (or `mingw32-make`, `nmake`, etc).

Now you can start Cura and test the plug-in.