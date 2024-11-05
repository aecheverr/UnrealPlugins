from unreal import(
    AssetToolsHelpers,
    AssetTools,
    EditorAssetLibrary,
    Material,
    MaterialFactoryNew,
    MaterialProperty,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSample2D,
    AssetImportTask,
    FbxImportUI
)

import os

class UnrealUtility:                                                                                                        #create a class for our unreal utility tools
    def __init__(self):
        self.substanceRootDir = "/game/Substance/"                                                                          #instantiate variables
        self.baseMaterialName = "M_SubstanceBase"
        self.substanceTempDir = "/game/Substance/Temp/"
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetallicName = "OcclusionRoughnessMetallic"
    
    def FindOrCreateBaseMaterial(self):                                                                                     #function to see if we have already created a base material and create one if we haven't already
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName,                                   #create new base color map and connect it to the material we created
                                                                   self.substanceRootDir, 
                                                                   Material, 
                                                                   MaterialFactoryNew())
        
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)                         #create new normal map and connect it to the material we created
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)

        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)           #create new oocclusion/roughness/metallic map and connect it to the material we created
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallicName)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC)

        EditorAssetLibrary.save_asset(baseMat.get_path_name())                                                              #automatically save material we created in unreal
        return baseMat
    
    def LoadMeshFromPath(self, meshPath):                                                                                   #creat function to find the file location and import a fbx mesh
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")
        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = "/game/" + meshName
        importTask.save = True
        importTask.automated = True

        fbximportOPtions = FbxImportUI()
        fbximportOPtions.import_mesh = True
        fbximportOPtions.import_as_skeletal = False
        fbximportOPtions.import_materials = False
        fbximportOPtions.static_mesh_import_data.combine_meshes = True

        importTask.options = fbximportOPtions

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]

    def LoadFromDir(self, fileDir):                                                                                         #create function to load a fbx mesh from a directory
        for file in os.listdir(fileDir):
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(fileDir, file))