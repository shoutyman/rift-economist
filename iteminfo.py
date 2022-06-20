#python imports
import json
import configparser

#local imports
import formulas

#load item data
config = configparser.ConfigParser()
config.read("config.ini")
itemdatafile = open(config["PATH"]["ITEMDATAPATH"])
itemData = json.loads(itemdatafile.read())
itemData = itemData["data"]

#returns the name and formula for the gold value of a given stat
def getStatFormula(stat):
    match stat:
            case "FlatHPPoolMod": #HP
                statName = "HP"
                recipe = formulas.getHealthValue
            case "FlatMPPoolMod": #mana
                statName = "Mana"
                recipe = formulas.getManaValue
            case "PercentHPRegenMod": #percent hp regen
                statName = "Health Regen"
                recipe = formulas.getHealthRegenValue
            case "PercentMPRegenMod": #% mana regen
                statName = "Mana Regen"
                recipe = formulas.getManaRegenValue
            case "FlatArmorMod": #armor
                statName = "Armor"
                recipe = formulas.getArmorValue
            case "FlatPhysicalDamageMod": #AD
                statName = "Attack Damage"
                recipe = formulas.getAttackDamageValue
            case "FlatMagicDamageMod": #AP
                statName = "Ability Power"
                recipe = formulas.getAbilityPowerValue
            case "FlatMovementSpeedMod": #movespeed
                statName = "Movement Speed"
                recipe = formulas.getMoveSpeedValue
            case "PercentMovementSpeedMod": #%movespeed
                statName = "% Movement Speed"
                recipe = formulas.getPercentMoveSpeedValue
            case "PercentAttackSpeedMod": #attack speed
                statName = "% Attack Speed"
                recipe = formulas.getAttackSpeedValue
            case "FlatCritChanceMod": #crit chance
                statName = "Critical Strike Chance"
                recipe = formulas.getCritChanceValue
            case "FlatCritDamageMod": #crit damage(from IE, passives)
                statName = "Critical Strike Damage"
                recipe = formulas.getUnknownStatValue
            case "FlatSpellBlockMod": #magic resist
                statName = "Magic Resist"
                recipe = formulas.getMagicResistValue
            case "rFlatGoldPer10Mod": #gold from support items
                statName = "Gold per 10 seconds"
                recipe = formulas.getUnknownStatValue
            case "FlatMagicPenetrationMod": #magic pen
                statName = "Magic Penetration"
                recipe = formulas.getMagicPenValue
            case "PercentMagicPenetrationMod": #% magic pen
                statName = "% Magic Penetration"
                recipe = formulas.getPercentMagicPenValue
            case "PercentLifeStealMod": #lifesteal
                statName = "Lifesteal"
                recipe = formulas.getLifestealValue
            case "PercentOmniVampMod": #spellvamp
                statName = "Omnivamp"
                recipe = formulas.getOmnivampValue
            case "FlatLethalityMod": #lethality
                statName = "Lethality"
                recipe = formulas.getLethalityValue
            case "AbilityHasteMod": #ability haste
                statName = "Ability Haste"
                recipe = formulas.getAbilityHasteValue
            case "PercentMoveSpeedMod": #% movespeed
                statName = "% Movement Speed"
                recipe = formulas.getUnknownStatValue
            case "PercentHealShieldPowerMod": #heal/shield power
                statName = "Heal/Shield Power"
                recipe = formulas.getHealShieldPowerValue
            case _:
                statName = ""
                recipe = formulas.getUnknownStatValue
    return (statName, recipe)

def getBuyPrice(itemid):
    index = str(itemid)
    item = itemData[index]
    return item["gold"]["total"]

#returns a dictionary containing the item's stats
def getItemStats(itemid):
    index = str(itemid)
    item = itemData[index]
    return item["stats"]

#calculates gold value of an item's base stats
def getItemValue(itemid):
    sum = 0
    #look up the item id
    index = str(itemid)
    item = itemData[index]
    print(item["name"])
    itemStats = item["stats"]
    for baseStat in itemStats:
        statInfo = getStatFormula(baseStat)
        statName = statInfo[0]
        statFormula = statInfo[1]
        print(f"{statName}: {itemStats[baseStat]}, worth {statFormula(itemStats[baseStat])} gold")
        sum += statFormula(itemStats[baseStat])
    print(f"Total = {sum} gold")
    mythicValue = getMythicPassiveValue(itemid)
    if (mythicValue > 0):
        print(f"Maximium mythic passive value: {mythicValue}")
    return sum

#returns the maximum gold value of an item's mythic passive
def getMythicPassiveValue(itemid):
    maxValue = 0
    index = str(itemid)
    item = itemData[index]
    if (item.get("mythic") == True):
        mythicStats = item["mythicBonus"]
        for stat in mythicStats:
            statInfo = getStatFormula(stat)
            statName = statInfo[0]
            statFormula = statInfo[1]
            maxValue += statFormula(mythicStats[stat] * 5)
    return (maxValue)

#returns the gold efficiency of a given item
def getGoldEfficiency(itemid):
    index = str(itemid)
    item = itemData[index]
    goldinfo = item["gold"]
    buyprice = goldinfo["total"]
    goldvalue = getItemValue(itemid)
    if (buyprice == 0):
        return -1
    else:
        return (goldvalue / buyprice) * 100

#returns the total gold value of a given list of items
def getInventoryValue(currentItems):
    sum = 0
    for item in currentItems:
        itemid = item['itemID']
        sum += getItemValue(itemid)
    return sum

#returns a list containing the gold values of each item in the item data file
def listItemValues():
    values = {}
    for item in itemData:
        value = getItemValue(item)
        values[item] = value
    print(values)

def listItemEfficiencies():
    efficiencies = {}
    for item in itemData:
        efficiency = getGoldEfficiency(item)
        efficiencies[item] = efficiency
    print(efficiencies)

if __name__ == "__main__":
    listItemEfficiencies()
