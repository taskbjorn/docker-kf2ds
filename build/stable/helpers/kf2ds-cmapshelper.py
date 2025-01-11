import configparser
import json

customMapsDictPath = "/home/kf2/.kf2ds/overrides/kf2ds-cmaplist.json"
gameConfigPath = "/home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFGame.ini"
engineConfigPath = "/home/kf2/.kf2ds/server/KFGame/Config/LinuxServer-KFEngine.ini"

def setWorkshopItem(cMapData, wsItems):
    print(f"Adding workshop entry for map {cMapData['Map Name']}")

    wsItems.append(cMapData['Workshop ID'])

def setMapSummary(cMapData):
    print(f"Adding map summary for map {cMapData['Map Name']}")

    gameCfg = configparser.RawConfigParser(strict = False)
    gameCfg.optionxform = str

    gameCfg.add_section(cMapData['WebAdmin Name'] + " KFMapSummary")
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'MapName', cMapData['Map Name'])
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'MapAssociation', "0")
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'ScreenshotPathName', "UI_MapPreview_TEX.UI_MapPreview_Placeholder")
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'bPlayableInSurvival', cMapData['Playable in Survival'])
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'bPlayableInWeekly', cMapData['Playable in Weekly'])
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'bPlayableInVsSurvival', cMapData['Playable in Versus Survival'])
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'bPlayableInEndless', cMapData['Playable in Endless'])
    gameCfg.set(cMapData['WebAdmin Name'] + " KFMapSummary", 'bPlayableInObjective', cMapData['Playable in Objective'])

    with open(gameConfigPath, 'a+') as configfile:
        gameCfg.write(configfile, space_around_delimiters = False)

def setMapList(cMapData, cMapsList, cMapsListNew):
    if cMapData['New Custom Map'] == "Yes":
        print(f"Adding map list entry for map {cMapData['Map Name']} in new custom maps section")
        cMapsListNew.append("\"" + cMapData['Map Name'] + "\"")
    else:
        print(f"Adding map list entry for map {cMapData['Map Name']} in custom maps section")
        cMapsList.append("\"" + cMapData['Map Name'] + "\"")

def main():
    # Read the custom maps dictionary
    with open(customMapsDictPath, "r") as json_dict:
        customMaps = json.load(json_dict)

    # Initialise lists
    wsItems = []
    cMapsList = []
    cMapsListNew = []

    for cMap, cMapData in customMaps.items():
        setWorkshopItem(cMapData, wsItems)
        setMapSummary(cMapData)
        setMapList(cMapData, cMapsList, cMapsListNew)
    
    # Write workshop entries to LinuxServer-KFEngine.ini
    print(f"Writing workshop entries to LinuxServer-KFEngine.ini")

    with open(engineConfigPath, 'a') as engineCfg:
        engineCfg.write("[OnlineSubsystemSteamworks.KFWorkshopSteamworks]\n")
        for wsItem in wsItems:
            engineCfg.write("ServerSubscribedWorkshopItems=" + wsItem + "\n")

    # Write maplist to LinuxServer-KFGame.ini
    print(f"Updating default maplist in LinuxServer-KFGame.ini")

    gameCfg = configparser.RawConfigParser(strict = False)
    gameCfg.optionxform = str

    gameCfg.read(gameConfigPath)

    mapList = gameCfg.get('KFGame.KFGameInfo', 'GameMapCycles')
    mapList = mapList[:7] + "\". , - *   *  - .  - ( OFFICIAL MAPS ) - , . - *   *  - , .\"," + mapList[7:-2] + ",\". , - *   *  - .  - ( NEW CUSTOM MAPS ) - , . - *   *  - , .\"," + ','.join(cMapsListNew) + ",\". , - *   *  - .  - ( CUSTOM MAPS ) - , . - *   *  - , .\"," + ','.join(cMapsList) + mapList[-2:]

    # Reinitialise parser
    gameCfg = configparser.RawConfigParser(strict = False)
    gameCfg.optionxform = str
    gameCfg.add_section('KFGame.KFGameInfo')
    gameCfg.set('KFGame.KFGameInfo', 'GameMapCycles', mapList)

    print(f"Final maplist:\n{mapList}")

    with open(gameConfigPath, 'a+') as configfile:
        gameCfg.write(configfile, space_around_delimiters = False)

if __name__ == "__main__":
    main()

