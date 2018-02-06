# Copyright (c) 2018 Ghostkeeper
# X3GWriter is released under the terms of the AGPLv3 or higher.

import subprocess
import os

from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry #To get the g-code from the GCodeWriter plug-in.
import UM.Platform

class X3GWriter(MeshWriter):
    known_machines = {
        "c3": "Cupcake Gen3 XYZ, Mk5/6 + Gen4 Extruder",
        "c4": "Cupcake Gen4 XYZ, Mk5/6 + Gen4 Extruder",
        "cp4": "Cupcake Pololu XYZ, Mk5/6 + Gen4 Extruder",
        "cpp": "Cupcake Pololu XYZ, Mk5/6 + Pololu Extruder",
        "cxy": "Core-XY with HBP - single extruder",
        "cxysz": "Core-XY with HBP - single extruder, slow Z",
        "cr1": "Clone R1 Single with HBP",
        "cr1d": "Clone R1 Dual with HBP",
        "r1": "Replicator 1 - single extruder",
        "r1d": "Replicator 1 - dual extruder",
        "r2": "Replicator 2 (default)",
        "r2h": "Replicator 2 with HBP",
        "r2x": "Replicator 2X",
        "t6": "TOM Mk6 - single extruder",
        "t7": "TOM Mk7 - single extruder",
        "t7d": "TOM Mk7 - dual extruder",
        "z": "ZYYX - single extruder",
        "zd": "ZYYX - dual extruder",
        "fcp": "FlashForge Creator Pro"
    }
    default_machine = "r1"
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

        command = [binary_filename, "-p"]

        container_stack = Application.getInstance().getGlobalContainerStack()
        if container_stack.getProperty("machine_gcode_flavor", "value") == "Makerbot":
            command.append("-g")
        machine = container_stack.getMetaDataEntry("machine_x3g_variant")
        if not machine in X3GWriter.known_machines:
            machine = X3GWriter.default_machine
            Logger.log("d", "Using default machine because machine_x3g_variant metadata was missing or invalid: %s (%s)", str(machine), X3GWriter.known_machines[machine])
        else:
            Logger.log("d", "Using configured machine: %s (%s)", str(machine), X3GWriter.known_machines[machine])

        command.extend(["-m", machine])

        command.extend([temp_file, file_name])

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
