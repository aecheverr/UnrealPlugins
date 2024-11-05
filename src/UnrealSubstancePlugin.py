import tkinter.filedialog                                                                                           #imports for unreal connections
from unreal import ToolMenuContext, ToolMenus, ToolMenuEntryScript, uclass, ufunction
import sys
import os
import importlib
import tkinter

srcDir = os.path.dirname(os.path.abspath(__file__))                                                                 #create the source directory file
if srcDir not in sys.path:                                                                                          #if there is no source directory in the system path, create a new source directory
    sys.path.append(srcDir)

import UnrealUtilities                                                                                              #import more unreal utilities
importlib.reload(UnrealUtilities)                                                                                   #reload the import

@uclass()
class LoadFromDirEntryScript(ToolMenuEntryScript):                                                                  #create new class in order to load tool menu script from directory entry script
    @ufunction(override=True)
    def execute(self, context):
        window = tkinter.Tk()
        window.withdraw()
        fileDir = tkinter.filedialog.askdirectory()
        window.destroy()
        UnrealUtilities.UnrealUtility().LoadFromDir(fileDir)
        

@uclass()                                                                                                           #create new class that hold button to build base material in our plugin menu dropfown in unreal
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial()

class UnrealSubstancePlugin:                                                                                        #create new class for our plugin menu dropdown in unreal
    def __init__(self):
        self.subMenuName = "SubstancePlugin"
        self.subMenuLabel = "Substance Plugin"
        self.InitUI()
    
    def InitUI(self):                                                                                               #create function to initialize and add our UI we created to unreal
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Substance Plugin")
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript())
        ToolMenus.get().refresh_all_widgets()
    
    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label)
        script.register_menu_entry()

UnrealSubstancePlugin()