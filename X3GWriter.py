# Copyright (c) 2017 Ghostkeeper
# This plug-in is released under the terms of the AGPLv3 or higher.

import subprocess
import os
import tempfile
import typing

from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
from UM.Application import Application
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
        #Get the g-code.
        scene = Application.getInstance().getController().getScene()
        gcode_list = getattr(scene, "gcode_list")
        if not gcode_list:
            Logger.log("e", "There is no g-code to write.")
            return False

        #Write the g-code to the temporary file.
        temp_gcode = None
        try:
            temp_gcode = tempfile.NamedTemporaryFile("w", delete=False)
            for gcode in gcode_list:
                temp_gcode.write(gcode)
            temp_gcode.close()
            temp_cfg = None
            try:
                temp_cfg = tempfile.NamedTemporaryFile("w", delete=False)
                self.write_cfg(temp_cfg)
                temp_cfg.close()
                temp_x3g = None
                try:
                    temp_x3g = tempfile.NamedTemporaryFile("r", delete=False)
                    temp_x3g.close()
                    command = self.gpx_command(temp_cfg.name, temp_gcode.name, temp_x3g.name)
                    try:
                        process = subprocess.Popen(command)
                        process.wait() #Wait until it's done converting.
                        output = process.communicate(b"y")
                        Logger.log("d", str(output))
                    except EnvironmentError as e:
                        Logger.log("e", "System call to X3G converter application failed: {error_msg}".format(error_msg=str(e)))
                        os.remove(temp_x3g.name)
                        os.remove(temp_cfg.name)
                        os.remove(temp_gcode.name)
                        return False
                    #Read from the temporary X3G file and put it in the stream.
                    stream.write(open(temp_x3g.name, "rb").read())

                except EnvironmentError as e:
                    if temp_x3g:
                        Logger.log("e", "Error writing temporary X3G file {temp_x3g}: {error_msg}".format(temp_x3g=temp_x3g, error_msg=str(e)))
                        os.remove(temp_x3g.name)
                    else: #The NamedTemporaryFile constructor failed.
                        Logger.log("e", "Error creating temporary X3G file: {error_msg}".format(error_msg=str(e)))
                    os.remove(temp_x3g.name)
                    os.remove(temp_cfg.name)
                    os.remove(temp_gcode.name)
                    return False
            except EnvironmentError as e:
                if temp_cfg:
                    Logger.log("e", "Error writing temporary configuration file {temp_cfg}: {error_msg}".format(temp_cfg=temp_cfg, error_msg=str(e)))
                    os.remove(temp_cfg.name)
                else: #The NamedTemporaryFile constructor failed.
                    Logger.log("e", "Error creating temporary configuration file: {error_msg}".format(error_msg=str(e)))
                os.remove(temp_gcode.name)
                return False
        except EnvironmentError as e:
            if temp_gcode:
                Logger.log("e", "Error writing temporary g-code file {file_name}: {error_msg}".format(file_name = temp_gcode.name, error_msg=str(e)))
                os.remove(temp_gcode.name)
            else: #The NamedTemporaryFile constructor failed.
                Logger.log("e", "Error creating temporary g-code file: {error_msg}".format(error_msg=str(e)))
            return False

        return True #No exceptions.

    ##  Gets the location of the executable to run for converting to X3G.
    def gpx_executable(self):
        gpx_path = os.path.dirname(os.path.realpath(__file__))
        if UM.Platform.Platform.isWindows():
            executable = "gpx.exe"
        elif UM.Platform.Platform.isOSX(): #For the cross-platform release, we need to disambiguate between MacOS and Linux.
            if os.path.isfile(os.path.join(gpx_path, "gpx_macos")): #Still fall back to the default name if the MacOS-specific file doesn't exist.
                executable = "gpx_macos"
            else:
                executable = "gpx"
        else: #Linux (hopefully).
            executable = "gpx"
        result = os.path.join(gpx_path, executable)
        result = os.path.expanduser(result)
        result = os.path.expandvars(result)
        Logger.log("d", "GPX executable: {executable_file}".format(executable_file=result))
        return result

    ##  Gets the command that we need to call GPX with.
    #
    #   \param configuration_file A file path to a configuration CFG file to run
    #   GPX with.
    #   \param gcode_file The input g-code file path.
    #   \param x3g_file The output X3G file path.
    #   \return A command to run GPX with, as list of parameters.
    def gpx_command(self, configuration_file, gcode_file, x3g_file) -> typing.List[str]:
        gpx_executable = self.gpx_executable()
        result = [gpx_executable, "-c", configuration_file, gcode_file, x3g_file]
        Logger.log("d", "GPX command: {command}".format(command=" ".join(result)))
        return result

    def write_cfg(self, cfg_stream):
        pass #TODO: Write the CFG file.

##  Removes the temporary g-code file that is an intermediary result.
#
#   This should be called at the end of the write, also if the write failed.
#   \param temp_file The URI of the temporary file.
def _removeTemporary(temp_file):
    try:
        os.remove(temp_file)
    except:
        Logger.log("w", "Couldn't remove temporary file %s", temp_file)
