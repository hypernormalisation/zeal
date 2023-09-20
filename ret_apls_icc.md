# Ret rotations and WoWSims APLs in ICC

There are two upcoming changes to the retribution rotation in Icecrown Citadel (ICC):
1. the inclusion of the Libram of Three Truths and its stacking strength buff, and
2. the ICC 2pc bonus

These, along with the very different stats on ICC gear and the powerful 4pc set bonus on judgements and seal damages, warrant a re-examination of Retribution paladin rotations and priority lists.

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

Once we arrive at an optimised rotation for this gear set, we can cross-check if other ICC gear sets favour different rotations (and if necessary, investigate any functions of stats that can indicate what rotations a player should do given their current gear setup).

