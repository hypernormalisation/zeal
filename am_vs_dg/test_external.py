

am = [
    32.1,
    51.5,
    22.4,
    25.1,
    38.9,
    28.7,
    22.4,
    41.8,
    41.8,
    34.8,
    53.4,
    44.1,
    34.8,
    34.8,
    53.4,
    40.0,
    40.0,
    30.0,
    36.2,
    36.2,
    36.2,
    41.8,
    41.8,
    41.8,
    40.1,
    30.0,
    50.0,
    41.8,
    30.1,
    41.8,
    41.8,
    41.8,
    54.4,
    54.4,
    36.1,
    50.5,
    50.5,
    58.8,
    44.7,
    49.1,
    43.0,
    36.2,
    45.2,
    45.2,
    51.5,
    32.1,
    32.1,
    51.5,
    41.8,
    41.8,
    32.1,
    41.8,
    51.5,
    41.8,
    41.8,
    41.8,
    51.5,
    41.8,
    41.8,
    41.8,
]

dsac = [
35.7,
37.9,
37.9,
34.8,
26.7,
31.2,
37.9,
37.9,
33.0,
47.9,
40.4,
47.9,
44.1,
28.1,
28.1,
41.6,
41.6,
45.7,
37.9,
37.9,
44.1,
28.1,
44.0,
37.9,
45.7,
61.2,
45.7,
45.7,
41.6,
56.2,
41.6,
53.8,
53.8,
45.9,
64.6,
48.4,
59.2,
48.9,
53.3,
53.4,
45.7,
37.9,
37.9,
37.9,
45.7,
45.7,
53.4,
53.4,
45.7,
45.7,
45.7,
]

both = [
    53.4,
40.1,
45.7,
62.8,
47.8,
52.0,
56.2,
45.7,
52.0,
53.4,
56.2,
59.1,
48.9,
61.2,
53.4,
53.4,
37.9,
]

none = [
   22.4,
22.4,
18.5,
28.7,
22.4,
22.4,
12.7,
34.8,
16.2,
16.2,
25.5,
25.5,
25.5,
40.0,
30.0,
27.0,
34.2,
27.0,
22.4,
22.4,
30.1,
40.0,
32.1,
37.9,
36.2,
27.0,
33.7,
33.4,
36.2,
48.9,
32.1,
12.7,
41.8,
32.1,
22.4,
32.1,
22.4,
]

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

am_mean = np.mean(am)
am_std = np.std(am)
dsac_mean = np.mean(dsac)
dsac_std = np.std(dsac)
both_mean = np.mean(both)
both_std = np.std(both)
none_mean = np.mean(none)
none_std = np.std(none)

print(f'Average miti for AM   = ({am_mean:0.1f} +/- {am_std:0.1f})%')
print(f'Average miti for DSac = ({dsac_mean:0.1f} +/- {dsac_std:0.1f})%')
print(f'Average miti for both = ({both_mean:0.1f} +/- {both_std:0.1f})%')
print(f'Average miti for none = ({none_mean:0.1f} +/- {none_std:0.1f})%')

b = np.linspace(10.0, 65.0, num = 11)

plt.hist(am, bins=b, label = "AM", color = "blue")
plt.hist(dsac, bins=b, alpha = 0.8, label = "DG", color = "teal")
plt.title("Dsac vs AM total miti vs black hole explosion, 1 fight")
plt.xlabel("Average Mitigation (%)")
plt.ylabel("N")
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(2))
plt.legend()
plt.savefig('dg_vs_am.png')

plt.hist(none, bins=b, alpha = 0.6, label = "No External", color = "red")
plt.hist(both, bins=b, alpha = 0.9, label = "AM & DG", color = "green")
plt.legend()

plt.savefig('dg_vs_am_2.png')