import random
random.seed()

p_wf = 0.2
cd_cs = 6
cd_ds = 10
cd_judge = 8


def does_wf():
    i = random.uniform(0,1)
    if i < 0.2: return True
    return False
    # return random.choices(population=[True, False], weights=[0.2,0.8])


class Sim():

    def __init__(self, speed=3.3, iters=10e5, fight_time=90):
        # Config
        self.speed = speed
        self.iters = iters
        self.fight_time = fight_time
        self.debug = False

        # Properties
        self.p_soc = speed * 7/60


    @property
    def can_soc(self):
        if self.soc_icd_remaining > 0: return False
        return True

    def roll_soc(self):
        i = random.uniform(0,1)
        if i < self.p_soc: return True
        return False
        # return random.choices(population=[True, False], weights=[self.p_soc, self.p_no_soc])

    def process_soc(self,is_wf=False, context="swing"):
        if not self.can_soc: return
        if not self.roll_soc(): return
        # If we get here we've procced
        self.soc_procs = self.soc_procs + 1
        self.soc_icd_remaining = 1.0
        if is_wf:
            self.wf_soc_procs = self.wf_soc_procs + 1
            if context == "swing":
                self.wf_soc_from_swing = self.wf_soc_from_swing + 1
            elif context == "cs":
                self.wf_soc_from_cs = self.wf_soc_from_cs + 1

    def process_melee(self):
        self.melee_cd_remaining = self.speed
        self.melees = self.melees + 1
        self.process_soc()
        self.process_wf()

    def process_wf(self, context='swing'):
        if not self.can_wf: return
        if not does_wf(): return
        # if we get here wf procced
        self.melees = self.melees + 1
        self.melee_cd_remaining = self.speed
        print('procced wf')
        self.wfs = self.wfs + 1
        if context == "swing":
            self.wfs_from_swing = self.wfs_from_swing + 1
        elif context == "cs":
            self.wfs_from_cs = self.wfs_from_cs + 1
        self.wf_icd_remaining = 1.5
        self.process_soc(True, context=context)

    def get_time_to_next_event(self):
        """Finds out the soonest interesting event to process and returns the time to it."""
        tn = self.melee_cd_remaining
        # If on GCD, if we come off GCD before next swing, advance to that time instead.
        if self.gcd_remaining > 0:
            if self.gcd_remaining < tn:
                tn = self.gcd_remaining
        # If not on GCD and abilities are all on cooldown, maybe advance to nearest one.
        else:
            if self.cs_cd_remaining > 0:
                if self.cs_cd_remaining < tn:
                    tn = self.cs_cd_remaining
            if self.ds_cd_remaining > 0:
                if self.ds_cd_remaining < tn:
                    tn = self.ds_cd_remaining
            if self.judge_cd_remaining > 0:
                if self.judge_cd_remaining < tn:
                    tn = self.judge_cd_remaining
        return tn

    def process_abilities(self):
        if self.cs_cd_remaining <= 0:
            self.process_cs()
        if self.ds_cd_remaining <= 0:
            self.process_ds()
        if self.judge_cd_remaining <= 0:
            self.process_judge()

    def process_ds(self):
        if not self.gcd_remaining <= 0: return
        print(f"doing DS at t={self.t:0.2f}")
        self.ds_casts = self.ds_casts + 1
        self.ds_cd_remaining = 10.0
        self.gcd_remaining = 1.5
        self.process_wf(context="ds")

    def process_cs(self):
        if not self.gcd_remaining <= 0: return
        print(f"doing CS at t={self.t:0.2f}")
        self.cs_casts = self.cs_casts + 1
        self.cs_cd_remaining = 6.0
        self.gcd_remaining = 1.5
        self.process_wf(context="cs")

    def process_judge(self):
        if not self.gcd_remaining <= 0: return
        print(f'doing judge at t={self.t:0.2f}')
        self.judge_casts = self.judge_casts + 1
        self.judge_cd_remaining = 8
        self.gcd_remaining = 1.5
        self.process_wf(context="judge")

    def update_timers(self):
        tn = self.get_time_to_next_event()
        self.melee_cd_remaining = self.melee_cd_remaining - tn

        # GCD
        if self.gcd_remaining > 0:
            self.gcd_remaining = self.gcd_remaining - tn
        else:
            self.gcd_remaining = 0
        # ICDs
        if self.wf_icd_remaining > 0:
            self.wf_icd_remaining = self.wf_icd_remaining - tn
        else:
            self.wf_icd_remaining = 0
        if self.soc_icd_remaining > 0:
            self.soc_icd_remaining = self.soc_icd_remaining - tn
        else:
            self.soc_icd_remaining = 0
        # Actives
        if self.cs_cd_remaining < 0:
            self.cs_cd_remaining = 0
        else:
            self.cs_cd_remaining = self.cs_cd_remaining - tn
        if self.ds_cd_remaining < 0:
            self.ds_cd_remaining = 0
        else:
            self.ds_cd_remaining = self.ds_cd_remaining - tn
        if self.judge_cd_remaining < 0:
            self.judge_cd_remaining = 0
        else:
            self.judge_cd_remaining = self.judge_cd_remaining - tn

    @property
    def can_wf(self):
        if self.wf_icd_remaining > 0: return False
        return True

    def run(self):
        self.n_melee_list = []
        self.n_wf_list = []
        self.n_soc_list = []
        self.n_wf_soc_list = []
        self.n_wf_from_cs_list = []

        for i in range(self.iters):
            self.run_one_iter()

        # self.summarise_results()


    def run_one_iter(self):
        self.t = 0

        # Cooldowns
        self.melee_cd_remaining = 0
        self.ds_cd_remaining = 0
        self.cs_cd_remaining = 0
        self.judge_cd_remaining = 0

        # ICDs
        self.gcd_remaining = 0
        self.soc_icd_remaining = 0
        self.wf_icd_remaining = 0

        # Containers for current iter
        self.melees = 0
        self.wfs = 0
        self.wfs_from_swing = 0
        self.wfs_from_cs = 0

        self.soc_procs = 0
        self.wf_soc_procs = 0
        self.wf_soc_from_swing = 0
        self.wf_soc_from_cs = 0

        self.ds_casts = 0
        self.cs_casts = 0
        self.judge_casts = 0


        while self.t < self.fight_time:
            print(f"- Current time = {self.t:0.2f}")
            # First handle autos.
            if self.melee_cd_remaining <= 0:
                print('doing auto')
                self.process_melee()

            # If off GCD, process any abilities we need to
            if self.gcd_remaining <= 0:
                self.process_abilities()

            tn = self.get_time_to_next_event()
            print(f'waiting {tn:0.2f} seconds...')
            self.update_timers()

            self.t = self.t + tn

        print('-------')
        print(self.melees, self.wfs)
        print(self.soc_procs, self.wf_soc_procs)
        self.book_iter_results()

    def book_iter_results(self):
        self.n_melee_list.append(self.melees)
        self.n_wf_list.append(self.wfs)
        self.n_soc_list.append(self.soc_procs)
        self.n_wf_soc_list.append(self.wf_soc_procs)
        self.n_wf_from_cs_list.append(self.wfs_from_cs)

    def summarise_results(self):
        n_melee = sum(self.n_melee_list) / len(self.n_melee_list)
        n_wfs = sum(self.n_wf_list) / len(self.n_wf_list)
        n_soc = sum(self.n_soc_list) / len(self.n_soc_list)
        n_wf_soc = sum(self.n_wf_soc_list) / len(self.n_wf_soc_list)
        n_wf_cs = sum(self.n_wf_from_cs_list) / len(self.n_wf_from_cs_list)
        print(f"Number of melee attacks = {n_melee:0.2f}")
        print(f"Number of CS casts          = {self.cs_casts}")
        print(f"Number of DS casts          = {self.ds_casts}")
        print(f"Number of Judgement casts   = {self.judge_casts}")
        print(f"Ave number of wf procs      = {n_wfs:0.2f}")
        print(f"Ave number of wf procs from CS = {n_wf_cs:0.2f}")
        print(f"Ave number of SoC procs     = {n_soc:0.2f}")
        print(f"Ave bonus SoC procs from wf = {n_wf_soc:0.2f}")

if __name__ == "__main__":
    s = Sim(iters=10000, speed=4.0)
    s.run()

    s2 = Sim(iters=10000,speed=3.3)
    s2.run()
    print()
    print('4.0 speed:')
    s.summarise_results()
    print('-----------')
    print('3.3 speed:')
    s2.summarise_results()
    # s = Sim(iters=1, speed = 3.3)
    # s.run()
    # s.summarise_results()
    #
    # s = Sim(iters=1, speed = 4.0)
    # s.run()
    # s.summarise_results()
