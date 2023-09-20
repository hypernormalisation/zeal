# Ret rotations and WoWSims APLs in ICC


Moving into ICC, there are two primary gearing effects that could result in optimal ret rotations being different from previous phases:
1. the inclusion of the Libram of Three Truths and its stacking strength buff, and
2. the ICC 2pc bonus, which has a 40% chance to reset the cooldown of Divine Storm on a successful autoattack.

These, along with the very different stats on ICC gear and the powerful 4pc set bonus that boosts judgement and seal damage, warrant a re-examination of ret paladin rotations and priority lists.

The recently implemented WoWSims APL provides us with a powerful environment to test out rotational considerations with the new gear.
We can use this to arrive at some *effective and practical* rotational considerations that rets who want to optimise their damage output might find useful in ICC; this is to say, considerations a player could actually follow in a real raid situation with the use of weak auras or addons to help timing.

This note uses release v0.1.48 of WoWSims.

## General considerations

The sim has a lot of free variables, even for a relatively simpler spec like ret.
As such, we should work out a sensible set of initial conditions we'll work with.

### Gearing

As regards gear, we'll start working with the P4 preset.
With the extensive work that has gone into finding best-in-slot (BiS) gear with the legacy rotation, we can probably assume that regardless of whatever rotation we arrive at in ICC, this gear will be exceptionally performant or indeed optimal.

The optimal rotation is also very often a function of stats.
Breakpoints exist for stats like haste and critical strike chance in World of Warcraft that can result in different rotations becoming more performant as a player.

While not realistic, to picture this imagine a ret paladin with very low critical strike chance.
Their Exorcism is guaranteed to crit against certain mob types, which means the relative damage of Exorcism vs, e.g. a Crusader Strike will be higher compared to a player with "normal" levels of crit for ICC gear (which itself varies depending on how much agility gear the player wears).

Once we arrive at an optimised rotation for this gear set, we can cross-check if other ICC gear sets favour different rotations (and if necessary, investigate possible functions of stats that can give ouputs indicating what rotations a player should do given their current gear setup).

### Sim settings

It is important when simming to ensure that one is measuring actual differences in dps, rather than any sim artefacts that can arise from the fight lengths.
Ret being a spec that largely spams abilities (and has an execute ability), it can be very sensitive to small differences in fight time.

Let's first use the legacy rotation to conduct a small test looking at the sensitivity of dps to fight length variance.

```
TEST 1: fight length variance and dps stability

Rotation type: Custom
All legacy options ticked.
Divine Plea threshold 75%
20k iterations
Confirmed 0% time OOM.
P4 gear presets.
Lich King Hc preset.
AM spec.

Rotation 1:
HoW > Judge > CS > DS > Cons > Exo > HW

90s +/- 5s   : 16869 dps
90s +/- 10s  : 16906 dps
90s +/- 15s  : 16936 dps
90s +/- 20s  : 16980 dps

Rotation 2:
Judge > HoW > CS > Cons > DS > Exo > HW

90s +/- 5s   : 16762 dps
90s +/- 10s  : 16801 dps
90s +/- 15s  : 16834 dps
90s +/- 20s  : 16866 dps

```

We can see in both cases a slight trend upwards in dps as the fight length variance increases.
In all fight ranges, the numbers of cooldowns usable across the board remains constant.
What is the explanation for this?

It could be that 90s fights simply produce a particularly unfavourable distribution of cast sequences, and shorter or longer fights than this have slightly more numbers of high-damage casts abilities like Judgement or HoW. If so, that isn't particularly indicative of anything actionable by a player in an encounter with an indeterminate fight time.

### Scanning fight length with different fight length variances

Our primary goal is to construct a good general-purpose rotation for ret in ICC.
Therefore in choosing fight length and its associated variance, we should aim to not construct settings that are particularly sensitive to very precise fight lengths.

A good way to probe this might be to examine how a particular rotation's dps changes as a function of fight length, for a variety of different FL variances.

```
TEST 2

Rotation 1: HoW > Judge > CS > DS > Cons > Exo
(removing Holy Wrath to ensure we don't OOM at longer fight lengths on legacy)

20k iterations

+/- 5s

70s  : 17349
75s  : 17198
80s  : 17048
85s  : 16894
90s  : 16731
95s  : 16663
100s : 16644
105s : 16620
110s : 16567
115s : 16462
120s : 16366
125s : 16364
130s : 16430
135s : 16493
140s : 16543
145s : 16594
150s : 16591
155s : 16518
160s : 16420
165s : 16323
170s : 16212
175s : 16100
180s : 15996

+/- 10s



```
