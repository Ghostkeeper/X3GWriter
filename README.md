# X3GWriter
X3G output plugin for Cura. This allows saving the slice output as an X3G file for Makerbot-family printers and Malyan.

## Support
X3GWriter theoretically supports Windows, MacOS and Linux. However, support for MacOS has never been tested.

## Installation
To install this plug-in follow the following steps:

1. Download the .zip file from Github: https://github.com/Ghostkeeper/X3GWriter/archive/master.zip
2. Open the .zip file with your favourite archiver application (e.g. 7-zip).
3. Extract the contents of the .zip archive to Cura's plug-in directory in your installation, e.g. `C:\Program Files\Cura\plugins`.
4. (Re)start Cura.

## Usage
Once installed, you should now be able to select X3G output for printers that support it. Try the Malyan M180 printer. Load a mesh, and save the output to a file. In the file dialogue, you should now be able to select the X3G format.

## Compiling
X3GWriter is compiled using CMake. Basically what this does is to compile its dependecy, GPX, and places it in the correct location when you install or package.

Compiling is done using the standard CMake workflow, namely:

1. (Advised) Create a directory to build in, with the command `mkdir build`, then `cd build`.
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
