# Copyright (c) 2018 Ghostkeeper
# X3GWriter is released under the terms of the AGPLv3 or higher.

import subprocess
import os

from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry #To get the g-code from the GCodeWriter plug-in.
import UM.Platform

class X3GWriter(MeshWriter):
    def __init__(self):
        super().__init__()
        self._gcode = None

    ##  Write the X3G data to a stream.
    #
    #   \param stream The stream to write X3G data to.
    #   \param nodes A sequence of nodes to write to the stream.
    #   \param mode The output mode to use. This is ignored, since it has no
    #   meaning.
    def write(self, stream, nodes, mode = MeshWriter.OutputMode.TextMode):
        if mode != MeshWriter.OutputMode.TextMode:
            Logger.log("e", "X3G Writer does not support non-text mode.")
            return False
        #Find an unused file name to temporarily write the g-code to.
        file_name = stream.name
        if not file_name: #Not a file stream.
            Logger.log("e", "X3G writer can only write to local files.")
            return False
        file_directory = os.path.dirname(os.path.realpath(file_name)) #Save the tempfile next to the real output file.
        i = 0
        temp_file = os.path.join(file_directory, "output" + str(i) + ".gcode")
        while os.path.isfile(temp_file):
            i += 1
            temp_file = os.path.join(file_directory, "output" + str(i) + ".gcode")

        #Write the g-code to the temporary file.
        try:
            with open(temp_file, "w", -1, "utf-8") as f:
                PluginRegistry.getInstance().getPluginObject("GCodeWriter").write(f, None) #Let the g-code writer write its g-code into the temp file.
        except:
            Logger.log("e", "Error writing temporary g-code file %s", temp_file)
            _removeTemporary(temp_file)
            return False

        #Call the converter application to convert it to X3G.
        Logger.log("d", "App path: %s", os.getcwd())
        Logger.log("d", "File name: %s", file_name)
        binary_path = os.path.dirname(os.path.realpath(__file__))
        binary_filename = os.path.join(binary_path, "gpx")
        if UM.Platform.Platform.isWindows():
            binary_filename += ".exe"
        if UM.Platform.Platform.isOSX(): #For the cross-platform release, we need to disambiguate between MacOS and Linux.
            if os.path.isfile(binary_filename + "_macos"): #Still fall back to the default name if the MacOS-specific file doesn't exist.
                binary_filename += "_macos"

        command = [binary_filename, "-p", "-m", "r1d", "-c", os.path.join(binary_path, "cfg.ini"), temp_file, file_name]
        safes = [os.path.expandvars(p) for p in command]
        Logger.log("d", "Calling GPX: {command}".format(command=" ".join(command)))
        stream.close() #Close the file so that the binary can write to it.
        try:
            process = subprocess.Popen(safes)
            process.wait()
            output = process.communicate(b"y")
            Logger.log("d", str(output))
        except Exception as e:
            Logger.log("e", "System call to X3G converter application failed: %s", str(e))
            _removeTemporary(temp_file)
            return False

        _removeTemporary(temp_file)
        return True

##  Removes the temporary g-code file that is an intermediary result.
#
#   This should be called at the end of the write, also if the write failed.
#   \param temp_file The URI of the temporary file.
def _removeTemporary(temp_file):
    try:
        os.remove(temp_file)
    except:
        Logger.log("w", "Couldn't remove temporary file %s", temp_file)
