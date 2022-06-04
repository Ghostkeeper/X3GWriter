1.1.13 - Bug Fixes
====
* Incremented SDK version to work with Cura 5.0.

1.1.12 - Bug Fixes
====
* Fixed bug where GPX would crash if the start or end g-code contains characters not in ASCII-7.
* Improved error messages if something would go wrong (e.g. file permissions).
* Update GPX executables on all platforms to version 2.6.8.

1.1.11 - Bug Fixes
====
* Incremented SDK version to work with Cura 4.4.

1.1.10 - Bug Fixes
====
* Fixed getting maximum Z feedrate in Cura 4.2.
* Automated installation in latest release using CMake.

1.1.9 - Bug Fixes
====
* Changed SDK version to use the new way of listing SDK versions, to allow the plug-in to load with future versions of Cura.

1.1.8 - Bug Fixes
====
* Incremented SDK version to work with Cura 4.0.

1.1.7 - Bug Fixes
====
* Fixed a bug that would prevent the GPX executable from being updated in future releases.

1.1.6 - No-op release
====
* Just had to increment the version number because Cura's new Marketplace portal was buggy. This plug-in was used as a pilot for this Marketplace.

1.1.5 - No-op release
====
* Just had to increment the version number because Cura's new Marketplace portal was buggy. This plug-in was used as a pilot for this Marketplace.

1.1.4 - Bug Fixes
====
* Fixed logging GPX output on Windows, so that bugs can be traced more easily.

1.1.3 - Bug Fixes
====
* Fixed bug with printers that don't have a pre-set configuration in GPX, where they were requesting settings from the extruders using a function that was renamed.
* Give execution permissions to GPX executable. This was preventing the plug-in from working on MacOS.

1.1.2 - Bug Fixes
====
* Incremented SDK version to work with Cura 3.5.

1.1.1 - Bug Fixes
====
* Use default GPX profiles for some printers. This should make these printers behave a bit better via X3GWriter.
* Update the icon. Make it a bit more pretty.

1.1.0 - Tranquility
====
This version introduces GPX settings that can be loaded from the printer definition. This allows the print to work correctly also for other printers than the Malyan M180.

Features
----
* If a printer definition file specifies `machine_x3g_variant` metadata, this variant causes the X3GWriter to use correct settings for the selected printer according to GPX, such as steps per millimetre, end stop location, etc.
* If no X3G variant is specified, GPX will be called with the correct settings from Cura's settings list, which also has all of the necessary information (since I sneaked that into the main Cura builds).
* Added an icon for Cura's "Toolbox".

Bug Fixes
----
* Cura will no longer crash if there is an error with a temporary file for any reason. Instead, an error will be shown in the log.

1.0.1 - Bug Fixes
====
* Support for Cura 3.2. This fix should still allow the plug-in to work on older Cura versions as well.

1.0.0 - Base
====
This is the initial stable release. It is made for Cura 2.7.

Features
====
* Support for Windows.
* Support for MacOS.

0.1.0 - A Small Stepper For Man
====
X3GWriter started out as the first non-Ultimaker Cura plug-in in existence, aside from the post-processing scripts made for legacy Cura.

Features
----
* An option is now available in the output file types to save the toolpath as X3G.
* Linux support only.
* GPX settings are chosen appropriate for the Malyan M180 printer.