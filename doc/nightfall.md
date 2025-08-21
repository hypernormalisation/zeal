# Nightfall
Nightfall is a craftable epic axe notable for its incredibly strong proc, Spell Vulnerability, granting 15% increased magic damage against the target for 5s. Nightfall's proc is confirmed by Blizz to be working at 2ppm, or a proc chance of 11.7%. The proc is physical and cannot be resisted, so does not have to roll negation like miss or dodge. These are confirmed in Aggrend's post on the forums:

- https://us.forums.blizzard.com/en/wow/t/nightfall-debuff-is-way-lower-than-2ppm-stated-across-the-board-from-classic-wowhead/445831/75

For a Ret paladin, Nightfall can be triggered by your auto-attacks, your SoC and SoR procs, and your damaging judgements. A Ret seal-twisting between SoC and SoR, and using a variety of haste buffs, can achieve a surprisingly high uptime on the Spell Vulnerability proc.

While the raiding meta in Vanilla WoW is of course stacking as many fury warriors as is possible, casters still fulfil a role in optimised raid comps, and in more casual setups may feature significantly more caster DPS. As such, a player able to maintain Spell Vulnerability with reasonable uptime on a target is worth exploring for many guilds who might feature a ret paladin for fun or to make up for a shortfall in Blessing buffs.

## Per-swing proc chance

As stated before, auto-attacks, SoR procs, and SoC procs are all considered "melee attacks" by the game. This is determined not by the damage school type, but by the defense type the ability targets. So despite doing holy school damage, SoR/SoC procs are capable of proccing weapon procs.

Assuming striking the target from behind, auto-attacks can miss or be dodged (i.e. be negated)
Hit chance can be capped in classic at 100% for melee attacks, dodge chance is irreducable until TBC where expertise becomes an available stat.

We'll define

`p_hit = 1 - miss_chance - dodge_chance`

as the chance a melee attack lands.

- melee attacks of course roll this once
- for an SoR proc, if its inciting auto-attack connects there is no roll for negation, it's guaranteed to land.
- an SoC proc requires the inciting auto-attack to land, and then has to roll for negation again.

The Spell Vulnerability proc chance at 2ppm with a base weapon speed of 3.5 is

`p_sv = 2 * 3.5/60 ~= 0.117`

We'll calculate the per-swing chance to proc now assuming the ret is hitcapped and hitting from behind with a 6.5% chance to be dodged (that could be reduced to 6% by wearing Edgemaster's Handguards for +7 axe skill).

Therefore `p_hit = 0.935`.

### SoC only

SoC is 7ppm, meaning its proc chance is dynamic based on weapon speed:

`p_soc = 7 * base_weapon_speed / 60`

which is about 40% for Nightfall. Therefore the nightfall proc chance for a ret swinging with SoC up is 

`p_nfswing = (p_hit * p_sv) + (p_hit^2 * p_soc * p_sv)`

where the first term corresponds to autoattack, the second to the possible SoC proc. Plugging in numbers we get

`p_nfswing = 0.109` for SoC only.

### SoR only

```
p_nfswing = p_hit * 2 * p_sv
          = 0.218
```

### SoC/SoR twisting

```
p_nfswing = p_hit * (2 * p_sv + (p_hit^2 * p_soc * p_sv))
          = 0.257
```

So with SoC/SoR seal-twisting, you have a roughly one-quarter chance to proc Nightfall each swing.

## Proc uptime

The expected uptime can be expressed in the following way: 

> "at any random observation time, what is the chance of Nightfall being active, i.e. we've had a Nightfall proc in the last 5 seconds?"

To figure this out we need to know how many potential procs we could have had in that 5s. Nightfall procs resulting from your swings, and procs resulting from your judgement casts are largely independent, so we can treat them both seperately. Let's look at swings first.

### Swings
First we need to evaluate a swing frequency/duration based on your haste.

#### Swing Duration

`s = base_weapon_speed / product_of_all_haste_factors`

If you have e.g. 3% from counterweight that contributes a factor to the denominator of 1.03. You multiply that against all other sources of haste. The BiS setup has 3% counterweight, 1% from the head leg and glove slots each, and 15% from WCB. So the Nightfall swing time without additional procs is:

`s = 3.5 / (1.03 * 1.01 * 1.01 * 1.01 * 1.15) ~= 2.87`

With Scrolls of Blinding Light active:

`s = 3.5 / (1.03 * 1.01 * 1.01 * 1.01 * 1.15 * 1.25) ~= 2.29`

We can weight these relative to the fight length to evaluate the expected uptime of the proc for any particular encounter.

If the ret does not have WCB or scrolls active:

`s = 3.5 / (1.03 * 1.01 * 1.01 * 1.01) ~= 3.3`

#### Swing Sampling

Now we have the swing frequency and the chance to proc per-swing, we can look at how many swings we'll have had in the past 5 seconds.

We express the Spell Vulnerability duration `D` via Euclidean (or remainder) division as:

`D = ms + r`

where `s` is the swing duration after haste effects, `m` is the number of whole swings, and `r` is some leftover duration.

Our uptime needs to know the probability of the proc being active *at a random time*, so there is some randomness in the number of swings that may have occurred in the previous 5s. We always have at least `m` swings in that duration, but depending on the swing speed and remaining duration, there could be an additional one for `m+1`.

For instance, if the BiS haste setup with scrolls active yields a swing duration of about 2.3s, we could have had 2 or 3 swings occur in the previous 5s depending on what time in the swing schedule we randomly chose. The probability for `m+1` swings is

`c = r / s = 0.4/2.3 = 0.174`

so a 17.4% chance that at any random time we had 3 swings in the previous 5s, and a 82.6% chance we had only 2 at this swing duration.

#### Swing uptime expression

We now have all the pieces to express the uptime from swings.

The chance for no proc in the last D seconds is `(1-q)^m` where `q` is the Spell Vulnerability chance per swing, and `m` is the number of swings.

In the last D seconds, we had `m` swings with probability `c` and `m+1` swings with probability `(1-c)`.

The uptime is the relative mixture of these two possibilities occuring, subtracted from 1 to give the chance of any proc having happened on those swings:

`U = 1 - c(1-q)^(m+1) - (1-c)(1-q)^m`

The uptime from swings at the relevant haste points are therefore:

- Enchants + WCB + Scrolls -> 47.4%
- Enchants + WCB -> 43.4%
- Enchants only -> 39.3%

### Judgements

Judgement of Command can also proc Spell Vulnerability with the same proc chance. It has a 10s cooldown, down to 8s with the Improved Judgements Ret talent.

Let's imagine that you're judging with an average interval J. Because Judgement's minimum cooldown is 8s and Nightfall's proc is 5s, we can have at most 1 Judgement cast in the previous 5s, so a simplified logic that we applied to swings also applies to judgements.

The probability `p_j` of having a judgement cast in the past period `D` is simply

`p_j = D / J`

Judgement of command due to a quirk in the spell tables rolls on spell hit, which has a 17% chance to miss by default. We'll assume the ret has no source of spell hit on gear and this applies in full.

Taking `p_jhit` as 0.83 the chance of no Spell Vulnerability proc from a judgement is

`p_nojudge = 1 - (D/J * p_jhit * p_nf)`

