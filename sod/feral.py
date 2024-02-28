import random

# Haste constants
cw = 1.03  # counterweight
wb = 1.1  # worldbuff
lw = 1.1  # LW gloves/helm


def does_wf():
    return random.uniform(0,1) <= 0.2

class FeralACPSimmer():

    def __init__(self, n_iters = int(1e6), miss_chance = 0.03,):
        self.n_iters = n_iters
        self.miss_chance = miss_chance
        self.acp_autos = {
            True: 0,
            False: 0,
        }

    def does_hit(self):
        return random.uniform(0,1) < 1.0 - self.miss_chance - 0.06 # dodge chance

    def sim_once_acp(self, acp_active=True):

        n_autos = 0
        t = 0

        base_speed = 1.0
        mult = cw * wb * lw
        if acp_active:
            mult = mult * 1.5
        attack_speed = base_speed / mult

        wf_timer = 0.0
        turned_off_lw = False

        while t < 30:
            # Turn off lw haste buffs after 20s
            if t >= 20 and not turned_off_lw:
                attack_speed = attack_speed * lw
                turned_off_lw = True

            if self.does_hit():
                n_autos = n_autos + 1
                if wf_timer <= 0.0:
                    if does_wf():
                        wf_timer = 1.5
                        if self.does_hit():
                            n_autos = n_autos + 1
        
            t = t + attack_speed
            wf_timer = wf_timer - attack_speed

        return n_autos


    def run(self, acp=False):
        n_autos_total = 0
        for i in range(self.n_iters):
            n_autos_total = n_autos_total + self.sim_once_acp(acp)
        n_autos_ave = n_autos_total / self.n_iters
        self.acp_autos[acp] = n_autos_ave

    def get_bonus_damage(self, damage_per_auto=134):
        n_autos_noacp = self.acp_autos[False]
        n_autos_acp = self.acp_autos[True]
        diff = n_autos_acp - n_autos_noacp
        print(f"ACP bonus auto damage = {diff*damage_per_auto:0.01f}")

if __name__ == "__main__":

    sim = FeralACPSimmer()
    print("ACP active simmer")
    print("3% miss chance, full armor debuffs")
    print(f"running {sim.n_iters} iterations")
    sim.run()
    sim.run(True)
    print(f"fACP gave {sim.acp_autos[True] - sim.acp_autos[False]:0.1f} bonus attacks")

    for armor, auto in zip(["4000", "3000", "2000"], [134, 160, 197]):
        print("--------------")
        print(f'{armor} boss armor, {auto} per auto:')
        sim.get_bonus_damage(auto)


