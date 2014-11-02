# Prefabs2Blueprints by Vgr v0.1
# Converts a Space Engineers prefab to a blueprint
# Big thanks to Keen Software House
# P2B does not have any copyright, feel free to re-use and modify
# Please give credit to the original author

import getpass
import config
import os

retcodes = {
0: "Prefab convertion completed successfully.",
1: "Error: You cannot name your prefab 'bp.sbc'.",
2: "Error: NAME is not defined in config.",
3: "Error: {0} is not a folder.".format(config.NAME),
4: "Error: Too many files in {0}.".format(config.NAME),
5: "Error: Already a blueprint.",
6: "Error: No prefab was found.",
7: "Error: Could not read file.",
}

def main():

    path = "C:\\Users\\{0}\\AppData\\Roaming\\SpaceEngineers\\Blueprints\\local\\".format(getpass.getuser())

    if config.NAME.lower() == "bp.sbc":
        return 1

    if not config.DISPLAY_NAME:
        config.DISPLAY_NAME = "Nobody"
    if not config.NAME:
        return 2
    if not config.NEW_NAME:
        config.NEW_NAME = config.NAME

    oldpath = None

    for folder in os.listdir(path):
        if folder.lower() == config.NAME.lower() and os.path.isdir(path + folder):
            oldpath = path + folder + "\\"

    if not oldpath:
        return 3

    prefab = None

    if len(os.listdir(oldpath)) > 1:
        return 4

    for file in os.listdir(oldpath):
        if file[-4:] == ".sbc":
            prefab = file
            break

    if prefab == "bp.sbc":
        return 5

    if not prefab:
        return 6

    old = open(oldpath + prefab, "r")
    new = open(oldpath + "bp.sbc", "w")

    oldlines = old.readlines()
    if not oldlines:
        return 7

    new.write(oldlines.pop(0) + oldlines.pop(0))
    new.write("  <ShipBlueprints>\n    <ShipBlueprint>\n")

    oldlines = oldlines[2:]
    new.write(oldlines.pop(0))

    new.write("        <TypeId>MyObjectBuilder_ShipBlueprintDefinition</TypeId>\n")
    new.write("        <SubtypeId>{0}</SubtypeId>\n".format(config.NEW_NAME))

    oldlines = oldlines[2:]
    new.write(oldlines.pop(0))
    new.write("      <DisplayName>{0}</DisplayName>\n".format(config.DISPLAY_NAME))

    while oldlines[:-3]:
        if oldlines[0] == "              <ShareMode>All</ShareMode>\n":
            oldlines[0] = "              <ShareMode>None</ShareMode>\n"
        if oldlines[0] == "              <PilotRelativeWorld>\n":
            del oldlines[:4]
            oldlines[0] = "              <PilotRelativeWorld xsi:nil=\"true\" />\n"
        if oldlines[0] == "          <ConveyorLines>\n":
            new.write("          <DampenersEnabled>{0}</DampenersEnabled>\n".format("true" if config.DAMPENERS else "false"))
        if oldlines[0][:32] == "              <ConveyorLineType>" and oldlines[0][-20:] == "</ConveyorLineType>\n":
            new.write("              <Sections />\n")
        new.write(oldlines.pop(0))

    new.write("      <WorkshopId>0</WorkshopId>\n      <OwnerSteamId>76561198050103334</OwnerSteamId>\n") # '76561198050103334' is Nobody
    new.write("    </ShipBlueprint>\n  </ShipBlueprints>\n</Definitions>")

    old.close()
    new.close()

    os.rename(oldpath, path + config.NEW_NAME)
    os.remove(path + config.NEW_NAME + "\\" + prefab)

    return 0

if __name__ == "__main__":
    print(retcodes[main()])
    os.system("pause")