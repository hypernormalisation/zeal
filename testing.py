
def get_d(ap):
    median = (549. - 365) / 2
    return (median + (ap*3.6)/14) * 1.06 * 1.03 * 1.02

def get_phys_d(d, p_crit, p_dodge):
    return d * ( 0.24*0.75 + p_crit * 2.06) + d * ((1 - 0.24 - p_crit - p_dodge)/(1 - p_dodge))
