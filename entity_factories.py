from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.levels import Level
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200)
    )

goblin = Actor(
    char="g",
    color=(63, 127, 63),
    name="Goblin",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    
    )

ogre = Actor(
    char="O",
    color=(255, 0, 0),
    name="Ogre",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    )



confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Scroll of Confusion",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Healing Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Scroll of Lightning Bolt",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=7),
)

pyroclasm_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Scroll of Pyroclasm",
    consumable=consumable.FireBallDamageConsumable(damage=25, radius=3),
)

dagger = Item(
    char=";",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger(),
)

sword = Item(
    char="/",
    color=(0, 0, 255),
    name="Sword",
    equippable=equippable.Sword(),
)

battle_axe = Item(
    char="?",
    color=(255, 0, 0),
    name="Battle Axe",
    equippable=equippable.BattleAxe(),
)

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="(",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail(),
)

plate_mail = Item(
    char="{",
    color=(139, 69, 19),
    name="Plate Mail",
    equippable=equippable.PlateMail()
)