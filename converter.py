# Prefabs2Blueprints by Vgr v0.3
# Converts a Space Engineers prefab to a blueprint
# Big thanks to Keen Software House
# P2B does not have any copyright, feel free to re-use and modify
# Please give credit to the original author
# v0.1 - First release
# v0.2 - Batch mode added
# v0.3 - Backwards compatibility with Python 2 & improved handling

import getpass
import config
import os

path = "C:/Users/%s/AppData/Roaming/SpaceEngineers/Blueprints/local/" % getpass.getuser()

retcodes = (
"Prefab convertion completed successfully.",
"Error: You cannot name your prefab 'bp.sbc'.",
"Error: NAME is not defined in config.",
"Error: %s is not a folder." % config.NAME,
"Error: Too many files in %s." % config.NAME,
"Error: Already a blueprint.",
"Error: No prefab was found.",
"Error: Could not read file.",
"Error: %s is not a folder." % config.BATCH_PATH,
"All prefabs converted successfully.",
)

def main():
    if config.NAME.lower() == "bp.sbc":
        return 1

    if not config.DISPLAY_NAME:
        config.DISPLAY_NAME = "Nobody"
    if not config.NAME and not config.BATCH_PATH:
        return 2
    if not config.NEW_NAME:
        config.NEW_NAME = config.NAME
    if not config.OWNER:
        config.OWNER = 0
    if config.OWNER == 0:
        config.SHARING = "None"
    if config.SHARING not in ("None", "All"):
        config.SHARING = "None"
    if not os.path.isdir(config.BATCH_PATH):
        return 8
    if config.BATCH_PATH:
        config.BATCH_PATH = config.BATCH_PATH.replace("/", "\\")
        if not config.BATCH_PATH[-1:] == "\\":
            config.BATCH_PATH += "\\"

    oldpath = None

    if not config.BATCH_PATH:
        for folder in os.listdir(path):
            if folder.lower() == config.NAME.lower() and os.path.isdir(path + folder):
                oldpath = path + folder + "\\"

        if not oldpath:
            return 3

        if len(os.listdir(oldpath)) > 1:
            return 4

        prefab = None

        for file in os.listdir(oldpath):
            if file[-4:] == ".sbc":
                prefab = file
                break

        if prefab == "bp.sbc":
            return 5

        if not prefab:
            return 6

        with open(oldpath + prefab) as old:
            oldlines = old.readlines()
            if not oldlines:
                return 7

        do(oldpath + "bp.sbc" , oldlines, oldpath, path, prefab, "single")

        return 0

    else:
        files = []
        for file in os.listdir(config.BATCH_PATH):
            if file[-4:] == ".sbc":
                files.append(file)

        for reader in files:
            if not os.path.exists(path + config.PREPEND + reader[:-4] + config.APPEND):
                os.mkdir(path + config.PREPEND + reader[:-4] + config.APPEND)
            with open(config.BATCH_PATH + reader) as old:
                oldlines = old.readlines()
                if not oldlines:
                    continue

            do(path+config.PREPEND+reader[:-4]+config.APPEND+"\\bp.sbc", oldlines, None, None, reader, "multiple")

        return 9

def do(file, oldlines, oldpath, path, prefab, type):

    if type == "single":
        print("Converting Prefab to Blueprint . . .")
    else:
        print("Converting Prefab '%s' to Blueprint . . ." % prefab)

    try:
        with open(file, "w") as new:
            new.write(oldlines.pop(0) + oldlines.pop(0))
            new.write("  <ShipBlueprints>\n    <ShipBlueprint>\n")
        
            oldlines = oldlines[2:]
            new.write(oldlines.pop(0))
        
            new.write("        <TypeId>MyObjectBuilder_ShipBlueprintDefinition</TypeId>\n")
            new.write("        <SubtypeId>%s</SubtypeId>\n" % config.NEW_NAME)
        
            oldlines = oldlines[2:]
            new.write(oldlines.pop(0))
            new.write("      <DisplayName>%s</DisplayName>\n" % config.DISPLAY_NAME)
        
            if oldlines[0][:18] == "      <RespawnShip>" and oldlines[0][-15:] == "</RespawnShip>\n":
                del oldlines[0]

            while oldlines[:-3]:
                if oldlines[0][:25] == "              <ShareMode>" and oldlines[0][-13:] == "</ShareMode>\n":
                    oldlines[0] = "              <ShareMode>%s</ShareMode>\n" % config.SHARING
                if oldlines[0] == "              <PilotRelativeWorld>\n":
                    del oldlines[:4]
                    oldlines[0] = "              <PilotRelativeWorld xsi:nil=\"true\" />\n"
                if oldlines[0] == "          <ConveyorLines>\n":
                    new.write("          <DampenersEnabled>%s</DampenersEnabled>\n" % "true" if config.DAMPENERS else "false")
                if oldlines[0][:32] == "              <ConveyorLineType>" and oldlines[0][-20:] == "</ConveyorLineType>\n":
                    new.write("              <Sections />\n")
                new.write(oldlines.pop(0))
        
            new.write("      <WorkshopId>0</WorkshopId>\n      <OwnerSteamId>%s</OwnerSteamId>\n" % str(config.OWNER))
            new.write("    </ShipBlueprint>\n  </ShipBlueprints>\n</Definitions>")
    except IndexError:
        os.remove(file)
        print("Could not convert '%s'" % prefab)
        return

    if type == "single":
        os.rename(oldpath, path + config.NEW_NAME)
        os.remove(path + config.NEW_NAME + "\\" + prefab)

if __name__ == "__main__":
    print(retcodes[main()])
    os.system("pause")
