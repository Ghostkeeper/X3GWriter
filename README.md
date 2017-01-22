# X3GWriter
X3G output plugin for Cura. This allows saving the slice output as an X3G file for Makerbot-family printers and Malyan.

## Support
Currently only Windows is supported. This limitation is due to a binary executable being included in the source code. This should be built from source once upon a time, but this repository is currently just meant as a simple hack to support X3G as well.

## Installation
To install this plug-in follow the following steps:
1. Download the .zip file from Github: https://github.com/Ghostkeeper/X3GWriter/archive/master.zip
2. Open the .zip file with your favourite archiver application (e.g. 7-zip).
3. Extract the contents of the .zip archive to Cura's plug-in directory in your installation, e.g. `C:\Program Files\Cura\plugins`.
4. (Re)start Cura.

## Usage
Once installed, you should now be able to select X3G output for printers that support it. Try the Malyan M180 printer. Load a mesh, and save the output to a file. In the file dialogue, you should now be able to select the X3G format.