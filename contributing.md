Reporting bugs
--------------
Please report bugs in the [issues page of this repository](https://github.com/Ghostkeeper/X3GWriter/issues). Do not report bugs in the Cura repository; they will be closed there.

When reporting a bug, it helps to provide the following information:
* The version of X3GWriter you're using.
* The printer you've selected in Cura.
* Cura's log file (see [Cura's readme](https://github.com/Ultimaker/Cura#logging-issues) for instructions on where to find that).

Sometimes, the bug will have been caused by this plug-in's major dependency, [GPX](https://github.com/markwal/GPX). A typical symptom is that a file was saved properly with a file size of more than 0 bytes. If you have such a file, you might have better luck reporting the issue with GPX.

If a bug report would contain private information, such as a proprietary 3D model, you may also e-mail me: rubend at tutanota com.

Requesting features
-------------------
If you request support for a particular model of printer, I can't really help you because I probably don't have the printer at home or at work. I'm open for contributions to the code from people that do have the printer, though.

Other feature requests are welcome in the [issues page of this repository](https://github.com/Ghostkeeper/X3GWriter/issues).

Submitting pull requests
------------------------
If you want to submit GPX settings to support a particular model of printer, I suggest you add them to [GPX](https://github.com/markwal/GPX/blob/master/src/shared/std_machines.h) instead, as a preset. That way a broader audience will be able to use your configuration, such as Octoprint users.

Other pull requests will be subject to the following requirements (additionally to common sense):
* It does not slow down processing significantly, such as by parsing all g-code.
* The code style is similar to the rest of the code in this repository.
* Your code will be licensed under AGPL 3.0 like the rest of the code in this repository.