import zeal.data
import zeal.data as zd


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

    @property
    def median_weapon_dmg(self):
        return (self.max_dmg + self.min_dmg) / 2.0


class Player:
    """Class to contain player info."""
    weapon: Weapon
    expertise: int
    ap: float
    arm_pen: int
    crit_chance: float
    crit_dmg_factor: float
    bonus_wf_ap: float
    holy_spell_dmg: int

    two_hand_spec_factor = 1.06
    improved_sanctity_aura_factor = 1.02

    def __init__(self, expertise=18, ap=3400, arm_pen=0,
                 crit_chance=0.35, crit_dmg_factor=2.06,
                 weapon=None,
                 bonus_wf_ap=511.75, sp=0):
        self.expertise = expertise
        self.ap = ap
        self.crit_chance = crit_chance
        self.crit_dmg_factor = crit_dmg_factor
        self.bonus_wf_ap = bonus_wf_ap
        self.arm_pen = arm_pen
        self.holy_spell_dmg = sp

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

    @property
    def global_dmg_factor(self):
        return self.two_hand_spec_factor * self.improved_sanctity_aura_factor

    @property
    def median_weapon_dmg(self):
        return self.weapon.median_weapon_dmg


class Target:
    """Class to contain target information."""
    base_armor: int
    affected_by_ff: bool  # faerie fire
    affected_by_imp_ea: bool  # improved expose armor
    affected_by_sunder_armor: bool
    affected_by_coe: bool  # curse of recklessness
    affected_by_crusade: bool  # is the target a humanoid, demon or undead?
    expose_weakness_agi: int
    affected_by_jotc: bool

    def __init__(self, base_armor=6200, crusade=True, expose_weakness_agi=1200,
                 ff=True, imp_ea=True, sunder=True, coe=True, crusade=True, jotc=True):
        self.base_armor = base_armor
        self.affected_by_crusade = crusade
        self.affected_by_jotc = jotc
        self.expose_weakness_agi = expose_weakness_agi

        self.affected_by_ff = ff
        self.affected_by_coe = coe
        self.affected_by_sunder_armor = sunder
        self.affected_by_imp_ea = imp_ea

    @property
    def bonus_ap_on_attacks(self):
        return self.expose_weakness_agi / 4.0

    @property
    def bonus_holy_sp_on_attacks(self):
        bonus_sp = 0
        if self.affected_by_jotc:
            bonus_sp += 219
        return bonus_sp

    @property
    def global_dmg_factor(self):
        factor = 1.0
        if self.affected_by_crusade:
            factor = factor * 1.03
        return factor

    @property
    def modified_armor(self):
        """Return the modified boss armor after debuffs."""
        base = self.base_armor
        if self.affected_by_ff:
            base -= 610
        if self.affected_by_coe:
            base -= 800
        # Only subtract sunder armor if no IEA.
        if self.affected_by_imp_ea:
            base -= 3075
        elif self.affected_by_sunder_armor:
            base -= 2600
        return base


class CombatAnalyser:
    """Class to combine Player and Target information for calcs."""
    player: Player
    target: Target

    def __init__(self, player, target):
        self.player = player
        self.target = target

    ###########################################################################################
    # Properties to get the final stats where player and target are both relevant.
    ###########################################################################################
    @property
    def final_crit_chance(self):
        """Return the crit chance modifies by crit suppression."""
        return self.player.crit_chance - 0.03

    @property
    def final_armor(self):
        """Return the final armor value to be used in the damage calc."""
        return max(0, self.target.modified_armor - self.player.arm_pen)

    @property
    def final_ap(self):
        return self.player.ap + self.target.bonus_ap_on_attacks

    @property
    def final_holy_spell_dmg(self):
        return self.player.holy_spell_dmg + self.target.bonus_holy_sp_on_attacks

    ###########################################################################################
    # Properties for damage scaling factors.
    ###########################################################################################
    @property
    def phys_dmg_scale_factor(self):
        return 1 - ((self.final_armor + 1)/(467.5*73 - 22167.5))

    @property
    def holy_dmg_scale_factor(self):
        return 0.94 * 1.1

    @property
    def global_dmg_factor(self):
        return self.player.global_dmg_factor * self.target.global_dmg_factor

    ###########################################################################################
    # Properties for physical damages
    ###########################################################################################
    @property
    def d_ave(self):
        """Return the average damage of a weapon standard hit."""
        return (self.player.median_weapon_dmg + self.player.weapon.speed * self.final_ap / 14.0) * \
            self.phys_dmg_scale_factor * self.global_dmg_factor

    @property
    def autoattack_outcomes_factor(self):
        """Returns the damage scale factor for non-negated autoattacks accounting for glance, crit etc."""
        return (zeal.data.p_glance * zeal.data.d_glance + self.player.crit_dmg_factor * self.final_crit_chance
                + (1 - zeal.data.p_glance - self.player.dodge_chance - self.final_crit_chance)
                ) / (1 - self.player.dodge_chance)

    @property
    def d_phys(self):
        """Returns the average weapon damage accounting for hits, crits, glances, dodges."""
        return self.autoattack_outcomes_factor * self.d_ave

    @property
    def wf_d_ave(self):
        """Returns the average damage of a windfury attack standard hit."""
        return (self.player.median_weapon_dmg + self.player.weapon.speed * (self.final_ap + self.player.bonus_wf_ap)
                / 14.0) * self.phys_dmg_scale_factor * self.global_dmg_factor

    @property
    def wf_d_phys(self):
        """Returns the average damage of a windfury attack accounting for hits, crits, glances, dodges."""
        return self.autoattack_outcomes_factor * self.wf_d_ave

    @property
    def wf_factor(self):
        """Returns the windfury scale factor, i.e. the dmg ratio of a windfury attack over a normal attack."""
        return self.wf_d_ave / self.d_ave

    @property
    def d_ave_crusader_strike(self):
        """Returns the average damage of a Crusader Strike attack's standard hit."""
        return (self.player.median_weapon_dmg * 1.1 + 3.3 * self.final_ap / 14.0) * self.phys_dmg_scale_factor * \
            self.global_dmg_factor

    @property
    def d_crusader_strike(self):
        """The damage of a crusader strike that is not negated."""
        return self.special_attack_outcome_scale_factor * self.d_ave_crusader_strike

    ###########################################################################################
    # Properties for holy seal procs.
    ###########################################################################################
    @property
    def special_attack_outcome_scale_factor(self):
        """The outcomes factor for seal spells, using special attack table. Only accounts for hit and crit."""
        return self.final_crit_chance * self.player.crit_dmg_factor + 1 - self.final_crit_chance

    @property
    def soc_proc_dmg_normal_hit(self):
        """Returns the average damage of a SoC proc on a regular hit."""
        return self.holy_dmg_scale_factor * self.global_dmg_factor * (0.7 * self.d_ave + 0.2 *
                                                                      self.final_holy_spell_dmg)

    @property
    def soc_proc_dmg(self):
        """Returns the average damage of a SoC proc for all non-negated outcomes."""
        return self.special_attack_outcome_scale_factor * self.soc_proc_dmg_normal_hit

    @property
    def sob_proc_dmg_normal_hit(self):
        """Returns the average damage of a SoB proc on a regular hit."""
        return self.holy_dmg_scale_factor * self.global_dmg_factor * 0.35 * self.d_ave

    @property
    def sob_proc_dmg(self):
        """Returns the average damage of a SoB proc for all non-negated outcomes."""
        return self.special_attack_outcome_scale_factor * self.sob_proc_dmg_normal_hit

    ###########################################################################################
    # Functions to get average damage numbers.
    ###########################################################################################
    def get_naked_swing_dmg(self, wf=True):
        """The projected damage of a naked swing with or without windfury."""
        p_d = self.player.dodge_chance
        prob_wf = zd.p_wf if wf else 0
        dmg = (1 - p_d) * self.d_phys + (1 - p_d)**2 * prob_wf * self.wf_d_phys
        return dmg

    def get_cs_dmg(self):
        """The projected damage of a Crusader Strike attack."""
        return (1 - self.player.dodge_chance) * self.d_crusader_strike

    def get_soc_swing_dmg(self, wf=True):
        """The projected damage of a SoC swing with or without windfury."""
        p_d = self.player.dodge_chance
        p_wf = zd.p_wf if wf else 0
        p_soc = self.player.soc_proc_chance
        phys_dmg = (1 - p_d) * self.d_phys + (1 - p_d)**2 * p_wf * self.wf_d_phys
        holy_dmg = (1 - p_d)**2 * (1 + p_wf * (1-p_d)*(1-p_soc)) * p_soc * self.soc_proc_dmg
        return phys_dmg + holy_dmg

    def get_sob_swing_dmg(self, wf=True):
        """The projected damage of a SoB swing with or without windfury."""
        p_d = self.player.dodge_chance
        p_wf = zd.p_wf if wf else 0
        phys_dmg = (1 - p_d) * self.d_phys + (1 - p_d)**2 * p_wf * self.wf_d_phys
        holy_dmg = (1 - p_d)**2 * self.sob_proc_dmg + p_wf * (1 - p_d)**3 * self.sob_proc_dmg
        return phys_dmg + holy_dmg

    def get_twist_dmg(self, wf=True):
        """The projected damage of a twist swing with or without windfury."""
        p_d = self.player.dodge_chance
        p_wf = zd.p_wf if wf else 0
        p_soc = self.player.soc_proc_chance
        phys_dmg = (1 - p_d) * self.d_phys + (1 - p_d)**2 * p_wf * self.wf_d_phys
        holy_dmg = (1 - p_d)**2 * self.sob_proc_dmg + (1 - p_d)**3 * p_wf * self.sob_proc_dmg + \
                   (1 - p_d)**2 * (p_soc + (1-p_d)*(1-p_soc)*p_wf) * (self.soc_proc_dmg + (1-p_d)*self.sob_proc_dmg)
        return phys_dmg + holy_dmg
