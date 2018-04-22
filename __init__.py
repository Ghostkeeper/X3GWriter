# Copyright (c) 2018 Ghostkeeper
# X3GWriter is released under the terms of the AGPLv3 or higher

from . import X3GWriter

import UM.Mesh.MeshWriter
from UM.i18n import i18nCatalog
catalog = i18nCatalog("x3gwriter")

def getMetaData():
    return {
        "mesh_writer": {
            "output": [{
                "extension": "x3g",
                "description": catalog.i18nc("X3G Writer File Description", "X3G File"),
                "mime_type": "application/x3g",
                "mode": UM.Mesh.MeshWriter.MeshWriter.OutputMode.BinaryMode
            }]
        }
    }

def register(app):
    return { "mesh_writer": X3GWriter.X3GWriter() }