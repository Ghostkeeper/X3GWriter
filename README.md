# X3GWriter
X3G output plugin for Cura. This allows saving the slice output as an X3G file for printers based on the Sailfish firmware.

This plug-in takes the normal g-code output of Cura, and converts it using [GPX](https://github.com/Ghostkeeper/GPX) to the X3G format.

## Support
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

1. **Marketplace:** In Cura, go to the Marketplace and find X3GWriter in the list. Click it, then click on "install" and restart Cura.
2. **From package:** Go to the [releases](https://github.com/Ghostkeeper/X3GWriter/releases) page to download a plug-in package file. For some old releases of Cura, you'll need a different release of X3GWriter:
   * Cura 3.5 and up: The most recent release is always compatible, but you must select the correct SDK version:
     |Cura version|SDK|
     |------------|---|
     |3.5         |5  |
     |3.6         |5  |
     |4.0         |6  |
     |4.1         |6  |
   * Cura 3.4: v1.1.1
   * Cura 3.3: v1.1.1
   * Cura 3.2: v1.1.1
   * Cura 3.1: v1.0.0
   * Cura 3.0: v1.0.0
   * Cura 2.7: v1.0.0
   * Before Cura 2.7: Not supported.
3. **Building packages:** Download the latest source code [from Github](https://github.com/Ghostkeeper/X3GWriter/archive/master.zip), then in a terminal run `cmake . && make pack` to create a .curapackage file for each supported SDK version. Similar to the previous option, select the SDK version that fits your version of Cura and drag it onto the Cura window, then restart Cura.
4. **From source:** Download the latest source code [from Github](https://github.com/Ghostkeeper/X3GWriter/archive/master.zip). In Cura, click on "Help", "Show configuration folder". Navigate to the "plugins" subfolder and unpack the .zip file from Github there. Rename the folder to "X3GWriter" (removing any suffix that Github added such as "-master"). Restart Cura.

## Usage
Once installed, you should now be able to select X3G output for printers that support it. Try the Malyan M180 printer. Load a mesh, and save the output to a file. In the file dialogue, you should now be able to select the X3G format.

## Compiling
X3GWriter is compiled using CMake. Basically what this does is to compile its dependecy, GPX, and places it in the correct location when you install or package.

Compiling is done using the standard CMake workflow, namely:

1. (Recommended) Create a directory to build in, with the command `mkdir build`, then `cd build`.
2. Configure and generate with CMake with the command `cmake ..`.
3. If desired, change the install directory. For instance:
   1. Find the plugins directory of Cura, such as `C:\Users\<You>\AppData\Roaming\cura\<Version>\plugins` on Windows, `~/.local/cura/<Version>/plugins` on Linux or `/Library/Application Support/cura/<Version>/plugins` on MacOS.
   2. Open CMake configuration using `cmake-gui .` or `ccmake .`.
   3. Toggle the advanced options. In CMake-GUI this is done with a checkbox at the top. In ccmake this is with the `t` key.
   4. Change the variable `CMAKE_INSTALL_PREFIX` to the installation directory found at step 3.i.
4. Configure. In CMake-GUI this is done with the "Configure" button. In ccmake this is done with the `c` key.
   1. If there were any errors, this is likely when you need to resolve them. In particular, please check whether the X3G executable was found. If it wasn't found, you will need to point CMake to the location of your GPX executable (likely in your Program Files or /usr/local somewhere).
5. Generate. In CMake-GUI this is done with the "Generate" button. In ccmake this is done with the `g` key.
6. Compile. This depends on your compiler. With GCC this is the `make` command. With MinGW this is the `mingw32-make` command. With MSVC this is with the `nmake` command.
7. Install with the command `make install` (or `mingw32-make`, `nmake`, etc).

Now you can start Cura and test the plug-in.