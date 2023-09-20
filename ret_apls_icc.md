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
The answer is likely that at values above 90s, third procs of Death's Choice become possible, which counteracts the downward trend from spending less time under the effects of Bloodlust.

It could also be that 90s fights simply produce a particularly unfavourable distribution of cast sequences, and shorter or longer fights than this have slightly more numbers of high-damage casts abilities like Judgement or HoW. If so, that isn't particularly indicative of anything actionable by a player in an encounter with an indeterminate fight time.

### Scanning fight length with different fight length variances

Our primary goal is to construct a good general-purpose rotation for ret in ICC.
Therefore in choosing fight length and its associated variance, we should aim to not construct settings that are particularly sensitive to very precise fight lengths.

A good way to probe this might be to examine how a particular rotation's dps changes as a function of fight length, for a variety of different FL variances.

Sheet with such a test:
> https://docs.google.com/spreadsheets/d/1cT1D5g1Z6ErRWYnOoqpLjTG5APsxo6KRItxksmqVZAk/edit?usp=sharing

Relevant plot:

![ret1](https://github.com/hypernormalisation/zeal/blob/main/figs/ret1.png?raw=true)

The DPS structure visible in the lower time variance distributions arises primarily from subsequent cooldown and trinket uses becoming possible as the fight gets longer, which is offsetting less time being spent under bloodlust.

It is very hard to say if effects arising from average number-of-casts are particularly visible in these distributions.
It is perhaps possible that some additional, non-trinket related structure may be present in the 5s and 10s variance curves at a fight length of around 90s (the very sharp downswing at a mean time of 90s in particular); but we cannot be certain.

### When should we sim granular times, and broader times?

I would make the argument that simming at broader times is more useful when considering rotational optimisations.
We want a general-purpose rotation that is applicable to a wide variety of situations in ICC.
As such, we are less interested in edge effects arising from additional trinket procs, number of casts of Avenging Wrath/Hyperspeed Accelerator etc.

If you are in a top guild with *very specific kill times*, then very precise fight times may be useful in helping you make gear choices, but this is a very distinctly different goal from ours.

As such, we will proceed with 20s as our fight length variance.

### What fight length(s) should be chosen?

As I argued in the last note I wrote on this subject [available here](https://github.com/hypernormalisation/zeal/blob/main/ret_prios.md), there are advantages to simming at relatively high fight times (of around 5 minutes or more).

When constructing first-come-first-served rotations, we are very interested in how well the cooldown timings sync up, or *cooldown clash*.
Simming at high fight times allows us to better isolate effects of cooldown clash because things like:
- how well a particular rotation syncs up with execute phase
- numbers of casts under specific cooldowns or trinket procs
are much more pronounced in simulations of lower fight times.
Simming at a high fight time dilutes these.

It is also of great interest to see how openers compare in the rotation.
While ret's opener is quite simple, stacking the Three Truths libram buff and Seal of Vengeance are areas where optimisation can be found - for instance, one may wish to prioritise CS over certain other abilities only when the Three Truths buff is not yet fully stacked (or the stacks are about to time out).

We should probably therefore investigate lower fight times as well as larger ones, to get more pronounced and isolated measurements of how our opening sequences perform.

With this in mind, we should perhaps sim at times of 1 minute when testing opening sequences, and 5 minutes when we are trying to establish overall priority orders.

If we find good overall priority orders first, we can supercede these in our openers as further optimisations.

So let's start with some 5 minute simulations to get a feel for the different possible ability priorities.
We'll first need a basic APL skeleton.

We'll also need to consider mana usage on the simulation, especially after the fixes to the JoW proc rate and the increased casts of DS/HW we expect in ICC.

# Basic ability priorities

Let's do something a bit unorthodox; let's sim at a very high fight time, but give the player a very high MP5 value to ensure we don't run up against mana issues.
In this, I'm hoping to find basic rough priorities that sim quite well, that we can then tweak as we need to.

First, we'll construct a very basic APL:

![Basic APL 1]([image.png](https://github.com/hypernormalisation/zeal/blob/main/figs/basic_apl_1.png?raw=true))

- we prepot
- we cancel Chaos Bane
- Hand of Reckoning is cast on cooldown
- cooldowns are cast as they come up
- our basic prio is HoW > Judge > CS > DS > Exo > Cons (but only if 4s left of the fight) > Holy Wrath

Under these such conditions (link 2 in the above sheet) we see the following figures:

```
Legacy       : 15876 dps
Basic APL 1  : 15952 dps
```

Now, ofc the legacy rotation is doing things like casting plea to deal with mana limitations that don't exist, so the APL coming ahead here is no surprise.

