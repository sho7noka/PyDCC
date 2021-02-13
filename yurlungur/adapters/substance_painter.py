# coding: utf-8
u"""
Example :  "substance painter.exe" --mesh "E:\\MyMeshFolder\\MyMesh.obj" --mesh-map "E:\\ MyMeshFolder \\DefaultMaterial_ambient_occlusion.png"

--mesh <meshPath>
Mesh to load in the project.
Example (create a new project with a specific mesh) : "substance painter.exe" --mesh "E:\\MymeshFolder\\MyMesh.obj"
Example (update the mesh inside an existing project) :  "substance painter.exe" --mesh "E:\\MymeshFolder\\MyMesh.obj"   "E:\\ MyMeshFolder \\PainterProject.spp"

--mesh-map
Baked maps associated with the mesh (AO, Normal, Curvature). Can be specified multiple times. Nomenclature : TextureSetName_AdditionalMapSlot
Ambient occlusion =  ambient_occlusion
Curvature =  curvature
Normal =  normal_base
World Space Normal =  world_space_normals
Position =  position
Thickness =  thickness

ID = id
--split-by-udim	Create a texture set per UDIM tile.
--export-path	 Default export path where the outputs of the project will be exported.
--disable-version-checking
"""
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["substance_painter"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, end, _ = __App("substance_painter")._actions

    __all__ = ["run", "end"]
