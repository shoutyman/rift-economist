#python imports
import configparser
import json
import logging
import re

#local imports
import backend.statkey as statkey

#open the item data file
logging.info("Reading item data...")
config = configparser.ConfigParser()
config.read("config.ini")
itemdatafile = open(config["PATH"]["ITEMDATAPATH"])

#setup attribute and id dictionaries
itemData = itemdatafile.read()
rawDictionary = json.loads(itemData)
dataDictionary = {}
idDictionary = {}
for key in rawDictionary.keys():
    itemName = key
    itemID = rawDictionary[key].get('id')
    if (itemID):
        idDictionary[itemName] = itemID
        rawDictionary[key]['name'] = itemName
        dataDictionary[itemID] = rawDictionary[key]

#takes stat tuple and returns its gold value
def getValueOfStat(stat):
    match stat[0]:
        case statkey.HEALTH: #HP
            statName = "HP"
            recipe = statkey.HEALTH_VALUE
        case statkey.MANA: #mana
            statName = "Mana"
            recipe = statkey.MANA_VALUE
        case statkey.HEALTH_REGEN: #percent hp regen
            statName = "Health Regen"
            recipe = statkey.HEALTH_REGEN_VALUE
        case statkey.MANA_REGEN: #% mana regen
            statName = "Mana Regen"
            recipe = statkey.MANA_REGEN_VALUE
        case statkey.ARMOR: #armor
            statName = "Armor"
            recipe = statkey.ARMOR_VALUE
        case statkey.ATTACK_DAMAGE: #AD
            statName = "Attack Damage"
            recipe = statkey.ATTACK_DAMAGE_VALUE
        case statkey.ABILITY_POWER: #AP
            statName = "Ability Power"
            recipe = statkey.ABILITY_POWER_VALUE
        case statkey.FLAT_MOVEMENT_SPEED: #movespeed
            statName = "Movement Speed"
            recipe = statkey.FLAT_MOVEMENT_SPEED_VALUE
        case statkey.MOVEMENT_SPEED: #%movespeed
            statName = "% Movement Speed"
            recipe = statkey.MOVEMENT_SPEED_VALUE
        case statkey.ATTACK_SPEED: #attack speed
            statName = "% Attack Speed"
            recipe = statkey.ATTACK_SPEED_VALUE
        case statkey.CRIT_CHANCE: #crit chance
            statName = "Critical Strike Chance"
            recipe = statkey.CRIT_CHANCE_VALUE
        case statkey.MAGIC_RESISTANCE: #magic resist
            statName = "Magic Resist"
            recipe = statkey.MAGIC_RESIST_VALUE
        case statkey.GOLD_PER_10: #gold from support items
            statName = "Gold per 10 seconds"
            recipe = 0
        case statkey.FLAT_MAGIC_PENETRATION: #magic pen
            statName = "Magic Penetration"
            recipe = statkey.FLAT_MAGIC_PENETRATION_VALUE
        case statkey.MAGIC_PENETRATION: #% magic pen
            statName = "% Magic Penetration"
            recipe = statkey.MAGIC_PENETRATION_VALUE
        case statkey.LIFESTEAL: #lifesteal
            statName = "Lifesteal"
            recipe = statkey.LIFESTEAL_VALUE
        case statkey.OMNIVAMP: #spellvamp
            statName = "Omnivamp"
            recipe = statkey.OMNIVAMP_VALUE
        case statkey.LETHALITY: #lethality
            statName = "Lethality"
            recipe = statkey.LETHALITY_VALUE
        case statkey.ABILITY_HASTE: #ability haste
            statName = "Ability Haste"
            recipe = statkey.ABILITY_HASTE_VALUE
        case statkey.MOVEMENT_SPEED: #% movespeed
            statName = "% Movement Speed"
            recipe = statkey.MOVEMENT_SPEED_VALUE
        case statkey.HEAL_SHIELD_POWER: #heal/shield power
            statName = "Heal/Shield Power"
            recipe = statkey.HEAL_SHIELD_POWER_VALUE
        case _:
            statName = "Unknown"
            recipe = 0
    return (recipe * stat[1])

#returns the buy price of the item
def getBuyPrice(itemid):
    item = dataDictionary.get(itemid)
    if (item):
        buyprice = item.get('buy')
        if (buyprice):
            #if the item is a transforming item, use the buyprice of its previous form
            if (type(buyprice) != int):
                precursorName = re.sub(":>", "", buyprice)
                previousItemID = idDictionary[precursorName]
                buyprice = getBuyPrice(previousItemID)
        else:
            buyprice = 0
    else:
        #logging.warning(f"Could not find data for itemID {itemid}")
        buyprice = 0
    return buyprice

#calculates gold value of an item's base stats
def getItemValue(itemid):
    sum = 0
    #look up the item id
    index = str(itemid)
    item = itemdatafile[index]
    mythicValue = getMythicPassiveValue(itemid)
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