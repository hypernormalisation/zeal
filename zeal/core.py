import zeal.data


class Weapon:
    """Class to contain weapon info."""
    speed: float
    min_dmg: int
    max_dmg: int

    def __init__(self, label=None, speed=None, min_dmg=None, max_dmg=None):
        if label:
            weapon_stats = zeal.data.weapon_stats_dict.get(label)
            if not weapon_stats:
                raise ValueError('Weapon label not recognised.')
            self.speed = weapon_stats['speed']
            self.min_dmg = weapon_stats['min_dmg']
            self.max_dmg = weapon_stats['max_dmg']
        elif speed and min_dmg and max_dmg:
            self.speed = speed
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg
        else:
            raise ValueError('Weapon construction failed')

    @property
    def soc_proc_chance(self):
        return 7 * self.speed / 60


class Player:
    """Class to contain player info."""
    weapon: Weapon
    expertise: int
    ap: float

    def __init__(self, expertise=18, ap=2000,
                 crit_chance=0.3,
                 weapon=None):
        self.expertise = expertise
        self.ap = ap
        self.crit_chance = crit_chance

        if isinstance(weapon, Weapon):
            self.weapon = weapon
        elif isinstance(weapon, str):
            self.weapon = Weapon(label=weapon)

    @property
    def dodge_chance(self):
        return (26 - self.expertise) * 0.0025

    @property
    def soc_proc_chance(self):
        return self.weapon.soc_proc_chance


class Target:
    pass
