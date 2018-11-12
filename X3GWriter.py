# Copyright (c) 2018 Ghostkeeper
# X3GWriter is released under the terms of the AGPLv3 or higher.

import configparser #To write a CFG file as configuration for GPX.
import math #For PI.
import os
import stat #To give execute permissions to GPX.
import subprocess
import tempfile
import typing

import UM.Application #To get settings from the global stack.
from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
import UM.PluginRegistry #To get the g-code writer plug-in to obtain the g-code for us.
import UM.Platform
import cura.Settings.ExtruderManager

class X3GWriter(MeshWriter):
    ##  Write the X3G data to a stream.
    #
    #   \param stream The stream to write X3G data to.
    #   \param nodes A sequence of nodes to write to the stream.
    #   \param mode The output mode to use. This is ignored, since it has no
    #   meaning.
    def write(self, stream, nodes, mode = MeshWriter.OutputMode.TextMode):
        #Write the g-code to a temporary file.
        temp_gcode = None
        try:
            temp_gcode = tempfile.NamedTemporaryFile("w", delete=False)
            UM.PluginRegistry.PluginRegistry.getInstance().getPluginObject("GCodeWriter").write(temp_gcode, None)
            temp_gcode.close()
            temp_cfg = None
            machine = self.gpx_machine()

            if machine is None:
                try:
                    temp_cfg = tempfile.NamedTemporaryFile("w", delete=False)
                    self.write_cfg(temp_cfg)
                    temp_cfg.close()
                except EnvironmentError as e:
                    if temp_cfg:
                        Logger.log("e", "Error writing temporary configuration file {temp_cfg}: {error_msg}".format(temp_cfg=temp_cfg, error_msg=str(e)))
                        os.remove(temp_cfg.name)
                    else: #The NamedTemporaryFile constructor failed.
                        Logger.log("e", "Error creating temporary configuration file: {error_msg}".format(error_msg=str(e)))
                    os.remove(temp_gcode.name)
                    return False
            else:
                Logger.log("d", "Using configured machine: %s (%s)", str(machine), X3GWriter.known_machines[machine])

            temp_x3g = None
            try:
                temp_x3g = tempfile.NamedTemporaryFile("r", delete=False)
                temp_x3g.close()
                temp_cfg_name = temp_cfg.name if temp_cfg is not None else None
                command = self.gpx_command(machine, temp_cfg_name, temp_gcode.name, temp_x3g.name)
                try:
                    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    process.wait() #Wait until it's done converting.
                    output = process.communicate(b"y")
                    Logger.log("d", str(output))
                except EnvironmentError as e:
                    Logger.log("e", "System call to X3G converter application failed: {error_msg}".format(error_msg=str(e)))
                    os.remove(temp_x3g.name)
                    if temp_cfg is not None:
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
                if temp_cfg is not None:
                    os.remove(temp_cfg.name)
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
        os.chmod(result, stat.S_IXUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        return result

    ##  Gets the command that we need to call GPX with.
    #
    #   \param machine The GPX machine to use or None. If given this takes precedence over configuration_file.
    #   \param configuration_file A file path to a configuration CFG file to run GPX with or None.
    #   \param gcode_file The input g-code file path.
    #   \param x3g_file The output X3G file path.
    #   \return A command to run GPX with, as list of parameters.
    def gpx_command(self, machine, configuration_file, gcode_file, x3g_file) -> typing.List[str]:
        result = [self.gpx_executable()]
        if machine is not None:
            global_stack = UM.Application.Application.getInstance().getGlobalContainerStack()
            if global_stack is not None and global_stack.getProperty("machine_gcode_flavor", "value") == "Makerbot":
                result.append("-g")
            result.extend(["-p", "-m", machine])
        else:
            result.extend(["-c", configuration_file])
        result.extend([gcode_file, x3g_file])
        Logger.log("d", "GPX command: {command}".format(command=" ".join(result)))
        return result

    # Machine types known to GPX.
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
        "zp": "ZYYX pro",
        "fcp": "FlashForge Creator Pro"
    }

    ## Gets the gpx machine type or none if unknown.
    def gpx_machine(self):
        global_stack = UM.Application.Application.getInstance().getGlobalContainerStack()
        machine = global_stack.getMetaDataEntry("machine_x3g_variant")
        return machine if machine in X3GWriter.known_machines else None

    ##  Fills a CFG file with settings to convert to X3G with.
    #
    #   \param cfg_stream A file stream that is supposed to get filled. All old
    #   data in the stream will get overwritten.
    def write_cfg(self, cfg_stream):
        application = UM.Application.Application.getInstance()
        global_stack = application.getGlobalContainerStack()
        extruder_stacks = application.getExtruderManager().getActiveExtruderStacks()
        parser = configparser.ConfigParser()

        parser.add_section("printer") #Slicer data.
        parser["printer"]["ditto_printing"] = "0" #Whether to duplicate the extrusion with all extruders. Cura doesn't support this.
        parser["printer"]["build_progress"] = "1" #Let GPX calculate the percent done counter shown on the printer's display.
        parser["printer"]["packing_density"] = "1.0" #TODO: 1.0 is the default but I don't know what this means. It's not documented.
        parser["printer"]["recalculate_5d"] = "1" #Whether to re-compute the extrusion widths. Please do! We assume that GPX knows better what to do with the feedrate than Cura.
        parser["printer"]["nominal_filament_diameter"] = str(extruder_stacks[0].getProperty("material_diameter", "value")) #Use the first extruder since it was used for actual slicing, not just matching materials.
        parser["printer"]["gcode_flavor"] = "makerbot" if global_stack.getProperty("machine_gcode_flavor", "value") == "Makerbot" else "reprap" #Default to RepRap for all other types.
        parser["printer"]["build_platform_temperature"] = str(global_stack.getProperty("material_bed_temperature", "value")) #Is different for layer 0 though!

        parser.add_section("x") #X axis.
        parser["x"]["max_feedrate"] = str(global_stack.getProperty("machine_max_feedrate_x", "value") * 60) #Maximum speed in this direction.
        parser["x"]["home_feedrate"] = str(global_stack.getProperty("speed_travel", "value") * 60) #Use normal travel speed to home with.
        parser["x"]["steps_per_mm"] = str(global_stack.getProperty("machine_steps_per_mm_x", "value")) #How many steps of the stepper motor results in 1mm of movement for the print head.
        parser["x"]["endstop"] = "0" if global_stack.getProperty("machine_endstop_positive_direction_x", "value") else "1" #0 if the endstop is at positive X rather than negative X.

        parser.add_section("y") #Y axis.
        parser["y"]["max_feedrate"] = str(global_stack.getProperty("machine_max_feedrate_y", "value") * 60)
        parser["y"]["home_feedrate"] = str(global_stack.getProperty("speed_travel", "value") * 60)
        parser["y"]["steps_per_mm"] = str(global_stack.getProperty("machine_steps_per_mm_y", "value"))
        parser["y"]["endstop"] = "0" if global_stack.getProperty("machine_endstop_positive_direction_y", "value") else "1"

        parser.add_section("z") #Z axis.
        parser["z"]["max_feedrate"] = str(global_stack.getProperty("max_feedrate_z_override", "value") * 60)
        parser["z"]["home_feedrate"] = str(global_stack.getProperty("max_feedrate_z_override", "value") * 60) #Always just go at maximum speed to home the build plate.
        parser["z"]["steps_per_mm"] = str(global_stack.getProperty("machine_steps_per_mm_z", "value"))
        parser["z"]["endstop"] = "0" if global_stack.getProperty("machine_endstop_positive_direction_z", "value") else "1"

        parser.add_section("a") #Right feeder (in the g-code labelled as T0).
        parser["a"]["max_feedrate"] = str(extruder_stacks[0].getProperty("machine_max_feedrate_e", "value") * 60) #Not configurable per extruder in Cura...
        parser["a"]["steps_per_mm"] = str(extruder_stacks[0].getProperty("machine_steps_per_mm_e", "value")) #How many steps of the stepper motor results in 1mm of filament movement.
        parser["a"]["motor_steps"] = str(extruder_stacks[0].getProperty("machine_feeder_wheel_diameter", "value") * math.pi * extruder_stacks[0].getProperty("machine_steps_per_mm_e", "value")) #Steps to make a full revolution of the feeder wheel.
        parser["a"]["has_heated_build_platform"] = str(int(extruder_stacks[0].getProperty("machine_heated_bed", "value"))) #Not configurable per extruder in Cura...

        parser.add_section("right") #Right extruder (in the g-code labelled as T0).
        parser["right"]["active_temperature"] = str(extruder_stacks[0].getProperty("material_print_temperature", "value"))
        parser["right"]["standby_temperature"] = str(extruder_stacks[0].getProperty("material_standby_temperature", "value"))
        parser["right"]["build_platform_temperature"] = str(extruder_stacks[0].getProperty("material_bed_temperature", "value")) #Not configurable per extruder in Cura...
        parser["right"]["actual_filament_diameter"] = str(extruder_stacks[0].getProperty("material_diameter", "value"))
        parser["right"]["packing_density"] = "1.0" #TODO: 1.0 is the default but I don't know what this is. It's not documented.

        if global_stack.getProperty("machine_extruder_count", "value") >= 2:
            parser.add_section("b") #Left feeder (in the g-code labelled as T1).
            parser["b"]["max_feedrate"] = str(extruder_stacks[1].getProperty("machine_max_feedrate_e", "value") * 60)
            parser["b"]["steps_per_mm"] = str(extruder_stacks[1].getProperty("machine_steps_per_mm_e", "value"))
            parser["b"]["motor_steps"] = str(extruder_stacks[1].getProperty("machine_feeder_wheel_diameter", "value") * math.pi * extruder_stacks[1].getProperty("machine_steps_per_mm_e", "value"))
            parser["b"]["has_heated_build_platform"] = str(int(extruder_stacks[1].getProperty("machine_heated_bed", "value")))

            parser.add_section("left") #Left extruder (in the g-code labelled as T1).
            parser["left"]["active_temperature"] = str(extruder_stacks[1].getProperty("material_print_temperature", "value"))
            parser["left"]["standby_temperature"] = str(extruder_stacks[1].getProperty("material_standby_temperature", "value"))
            parser["left"]["build_platform_temperature"] = str(extruder_stacks[1].getProperty("material_bed_temperature", "value"))
            parser["left"]["actual_filament_diameter"] = str(extruder_stacks[1].getProperty("material_diameter", "value"))
            parser["left"]["packing_density"] = "1.0"

        parser.add_section("machine")
        parser["machine"]["nominal_filament_diameter"] = str(extruder_stacks[0].getProperty("material_diameter", "value")) #Seems to be the same as the printer category.
        parser["machine"]["packing_density"] = "1.0" #Seems to be the same as the printer category.
        parser["machine"]["nozzle_diameter"] = str(extruder_stacks[0].getProperty("machine_nozzle_size", "value")) #The diameter of the nozzle seems to be quintessentially per-extruder, but GPX doesn't allow setting it per extruder. Just take one of them.
        parser["machine"]["extruder_count"] = str(global_stack.getProperty("machine_extruder_count", "value"))
        parser["machine"]["timeout"] = "20" #Let's just always home at most 20 seconds. This is what GPX uses for all built-in printers.
        #parser["machine"]["steps_per_mm"] = ? #I think the steps_per_mm per axis will override this.

        parser.write(cfg_stream)
