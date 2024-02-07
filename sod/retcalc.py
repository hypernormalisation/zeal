 
weapons_dict = {
    'pendulum': {
        'min': 124,
        'max': 187,
        'speed': 4.0,
        },
    'bloodlight': {
        'min': 116,
        'max': 175,
        'speed': 3.6,
        'str': 15,
        'ap': 32,
        'sp': 24,
        },
    'cleaver': {
        'min': 117,
        'max': 175,
        'speed': 3.3,
        'str': 29,
        'ap': 60
        }
    }

base_ap = 1000
base_sp = 300


def get_ave(d):
    return (d['min'] + d['max']) / 2

def get_bonus_ap(d, normalised = False):
    bonus_ap = d.get('ap', 0)
    ap = bonus_ap + base_ap
    speed = d['speed']
    if normalised: speed = 3.3
    return speed * ap / 14

def get_d_melee(weapon):
    d = weapons_dict[weapon]
    return get_ave(d) + get_bonus_ap(d)


def get_d_cs(weapon):
    d = weapons_dict[weapon]
    return (get_ave(d) + get_bonus_ap(d, True)) * 0.75

def get_d_ds(weapon):
    d = weapons_dict[weapon]
    return (get_ave(d) + get_bonus_ap(d)) * 1.1

def get_d_soc(weapon):
    d = weapons_dict[weapon]
    d1 = get_ave(d) + get_bonus_ap(d)
    d2 = base_sp * 0.29
    return (d1+d2)*0.7

def get_prob_soc(weapon, wf=True):
    d = weapons_dict[weapon]
    p = 7/60 * d['speed']
    if not wf: return p
    return p + (1-p)*p*0.2

def get_soc_procs_per_sec(weapon, wf=True):
    p = get_prob_soc(weapon, wf)
    return p / weapons_dict[weapon]['speed']

def get_dps_soc(weapon, wf=False):
    d = get_d_soc(weapon)
    return d * get_prob_soc(weapon, wf) / weapons_dict[weapon]['speed']

totals = {}

pendulum_attack_freq = (0.25*1.2 + 1/6 + 1/10 + 1/8)
pendulum_attack_freq_soc = (0.25*1.2 + 1/6 + 1/10 + 1/8 + get_soc_procs_per_sec('pendulum'))
pendulum_proc_dps = 300*pendulum_attack_freq_soc*0.016
print(pendulum_proc_dps)
# print (get_soc_procs_per_sec('pendulum'))

for k, v in weapons_dict.items():
    print(k)
    d_m = get_d_melee(k)
    dps_m = d_m/v['speed']
    d_cs = get_d_cs(k)
    dps_cs = d_cs/6
    d_ds = get_d_ds(k)
    dps_ds = d_ds / 10
    dps_soc = get_dps_soc(k, wf=True)* 0.88 * 1.1 * 0.94

    dps_total = dps_m + dps_cs + dps_ds + dps_soc
    if k == 'pendulum':
        dps_total = dps_total + pendulum_proc_dps
    totals[k] = dps_total
    print('melee hit:', d_m, ' dps: ', dps_m)
    print('cs:', d_cs, ' dps: ', dps_cs)
    print('ds:', d_ds, ' dps: ', dps_ds)
    print('soc dps basic wf:', dps_soc)
    print('total dps =', dps_total)
    print('*'*40)


exo_cd_pendulum = 8.77
exo_cd_bloodlight=8.22
exo_cd_cleaver=7.89


# print(exo_cd_cleaver/exo_cd_pendulum)
# print(exo_cd_pendulum/exo_cd_cleaver)


# print(d_melee('bloodlight')/d_melee('pendulum')*(4.0/3.6))
# print(d_ds('pendulum') / d_ds('cleaver'))
# print(dps_soc('pendulum')/dps_soc('cleaver'))
# print(dps_soc('pendulum', True)/dps_soc('cleaver', True))



