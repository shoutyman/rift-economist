#This file contains formulas for calculating gold values.
import backend.statkey as values
def getAttackDamageValue(attackDamage):
    return attackDamage * values.ATTACKDAMAGE_VALUE
 
def getAbilityPowerValue(abilityPower):
    return abilityPower * values.ABILITYPOWER_VALUE
 
def getArmorValue(armor):
    return armor * values.ARMOR_VALUE
 
def getMagicResistValue(magicResist):
    return magicResist * values.MR_VALUE
 
def getHealthValue(health):
    return health * values.HEALTH_VALUE
 
def getManaValue(mana):
    return mana * values.MANA_VALUE
 
def getHealthRegenValue(healthRegen):
    #1.0 health regen mod = 100% Health Regen
    return 100 * healthRegen * values.HEALTHREGEN_VALUE
 
def getManaRegenValue(manaRegen):
    #1.0 mana regen mod = 100% mana regen
    return 100 * manaRegen * values.MANAREGEN_VALUE
 
def getCritChanceValue(critChance):
    #the game represents crit chance as a value between 0 and 1
    return (critChance * 100) * values.CRITCHANCE_VALUE
 
def getAttackSpeedValue(attackSpeed):
    #game value = written value / 100
    #ex: the game represents 20% attack speed as 0.2
    return (attackSpeed * 100) * values.ATTACKSPEED_VALUE
 
def getMoveSpeedValue(moveSpeed):
    return moveSpeed * values.MOVESPEED_VALUE
 
def getLifestealValue(lifeSteal):
    return 100 * lifeSteal * values.LIFESTEAL_VALUE
 
def getPercentArmorPenValue(percentArmorPen):
    return 100 * percentArmorPen * values.PERCENTARMORPEN_VALUE
 
def getMagicPenValue(magicPen):
    return magicPen * values.MAGICPEN_VALUE
 
def getPercentMagicPenValue(percentMagicPen):
    return 100 * percentMagicPen * values.PERCENTMAGICPEN_VALUE
 
def getOnHitDmgValue(onHitDmg):
    return onHitDmg * values.ONHITDMG_VALUE
 
def getAbilityHasteValue(abilityHaste):
    return abilityHaste * values.ABILITYHASTE_VALUE
 
def getPercentMoveSpeedValue(percentMoveSpeed):
    return 100 * percentMoveSpeed * values.PERCENTMOVESPEED_VALUE
 
def getHealShieldPowerValue(healShieldPower):
    return 100 * healShieldPower * values.HEALSHIELDPOWER_VALUE
 
def getOmnivampValue(omnivamp):
    return 100 * omnivamp * values.OMNIVAMP_VALUE
 
def getLethalityValue(lethality):
    return lethality * values.LETHALITY_VALUE

#for stats without established gold values
def getUnknownStatValue(value):
    return 0
 