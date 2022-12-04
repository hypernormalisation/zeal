# A general-purpose priority for ret

## The limitations of evaluating prios

Sulis' new ret prioritiser tool lets us quickly evaluate priorities across a variety of fight lengths.
It's a great tool, and you can find the tool at:
https://thesorm.github.io/Ret-Prioritizer/

People are finding that the optimal rotations can vary significantly according to fight lengths, even when the variance in fight length is set to be quite high.

I believe that while useful, placing too much emphasis on these prio rankings at specifically *low fight times* might not be wise, for a couple of reasons.

### Ideal play in the final GCDs
You, as a player with a rough knowledge of how long in the encounter you have left, will play a fight differently than a basic prio system.

For instance, in a prio with Cons > Exo > HW (i.e. most good ones for clash resolution, sometimes including DS below Cons), you know not to cast a Consecrate over an available alternative when e.g. Noth the Plaguebringer is at 5% hp, because he's probably dying in about 2 GCDs, and you won't get enough consecrate ticks off for it to be worthwhile. The sim doesn't account for this, only casting according to prio.

There are also issues with certain fight times just "dividing into" your high cooldown abilities like Exo or HW particularly well, to the point where a 2-3s fight length change can increase your effective exo dps by a huge fraction by getting, say, 6 casts instead of 5 casts in the generated sequence.

### Variable Fight Length
Both the sim and Sulis' tool get around this to some extent by introducing variance to the fight length:
- the sim lets you select a central fight time and a variance, and then randomly selects a fight time each iteration with a uniform selection between the highest and lowest possible times.
- Sulis' tool scans the cast sequences generated at each timestep between the min and max fight times

This aims to produce enough different cast sequences from which to sample, that on average optimal and suboptimal setups get averaged out, and differences between overall numbers of casts at given thresholds get averaged out.

But... what fight length is required to totally get rid of these effects? The answer doesn't seem at all obvious to me.
Are suboptimal cast sequences vs optimal cast sequences periodic? If so, over what time interval do they average out? Are they instead more localised and in clumps?

The cast sequence at a given fight length, for a given prio, is always static. But this does not mean that the generated sequences between close fight times are similar. This is because the sim enters the execution phase at a different point in the rotation even across fight length changes of just 1-2s, and the fight after that point often looks totally different between say, 102s and 104s.

### Checking this out in actual cast sequences

I took a look at the cast sequences generated by the sim for 2 prios:
1. HoW > JoW > CS > DS > Cons > Exo > HW
2. HoW > JoW > CS > Cons > DS > Exo > HW

The scattering of suboptimal casts and threshold effects was often very localised with very few discernable patterns, even over 30-40s intervals.

For instance, the first prio had a particularly bad region of around 95-105s where it was consistently casting consecrate for its final GCD and getting between 0 and 2 ticks off, where either Exo or HW were available. The second prio didn't have this issue at all in that range.

So, someone simming a fight length of say, 90s +/- 15s, is going to find prio one artificially deflated in dps compared to prio two at the level of around 50-100dps, and might conclude that it's worth to prio Cons over DS in this situation, when in reality it probably doesn't matter very much at all.

## What simming at a given fight time range actually measures

When simming different fight lengths and evaluating different prios, you're conflating a bunch of different effects:
- the likelihood of suboptimal closers in the final GCDs
- how well the rotation syncs up with the execute phase on average across the fight range when played perfectly and without variance.
- how well the rotation syncs up with dps procs on your gear

But really, these factors are less important for actual play. We should all know how to close out a fight by casting any hard-hitting abilities off cooldown, or close to off cooldown. e.g. if I can cast a consecrate or alternately wait 1s for HoW to come off cooldown as the boss is dying, HoW is probably the better call because we're weighing up an almost guaranteed 700ish damage tick against a possible 9-10k nuke.

You also have to move in some fights and can no longer cast consecrate etc. You can have to cast a quick heal or a utility spell, and suddenly everything in your rotation desyncs. After that point, it's very hard to imagine what the new sequence looks like, and how long it takes for it to resync, if it even does at all.

As such, it's really not worthwhile in my opinion to try and derive optimal rotations at given fight times; real world fights have too much variance, and the sim conflates too many different, hard to measure things.

What we should perhaps do, is find an overall prio that consistently performs well, and stick to it.

### A note on adaptive prios
Sulis is already working on an adaptive prio to deploy in the tooling that will be very useful to this end.
Once it's validated there, it might make its way into his weak aura, which would be incredibly powerful.

Towards that end, let's try to isolate the general-purpose effects that actually make for a good prio.

# What makes a good prio?

In a FCFS rotation that attempts to maximise dps, you care about the following:
- maximising the number of high impact casts given the time available to you, especially when that time is short (e.g. execution phase)
- lowering the cooldown clash of abilities, and reducing the open GCD time (when you're off GCD but have no dps abilities to cast)
- lowering the "Effective Cooldown" of abilities in the rotation, where you generally want lower cooldown abilities used more quickly. For instance, if you delay CS by 3s, you effectively lose on average 50% of a CS cast in opportunity cost for casting other abilities. If you delay Exo by 3s, you comparatively lose 20% of an exo cast.

It'd be nice to have a "standard rotation" that performs well on paper and in the sim, that someone can use across all fight lengths, and to fall back upon when their rotation gets interrupted.

# Isolating cooldown clash with extreme fight times

Some of the above can be isolated by just running extremely long fights with high degrees of variance.
That way you really cut down on the effects of N cast edge effects (especially in execution phases with HoW), and patterns of suboptimal final casts arising over time ranges for a given prio.

This will let us isolate the effects of cooldown clash more efficiently.

Extreme fight times and variance help with:
- reducing consecrate clipping issues
- reduce edge effects around overall number of casts
- in particular for the above, reducing edge effects around HoW in execute phase

Let's run on Sulis' prio tool between 800s and 1200s, 0.5s timestep.
We'll use a miss chance of 0.5%, representative of most people's gearsets while training on one of the BiS or close-to-BiS P1 setups

We'll show the top 100 results for posterity at the bottom of this note.

For now let's take the top 20, and prune anything with judgement below third prio, because you might run into mana issues on longer fights. That gets rid of 3. The difference between the top and the bottom is about 19dps. This isn't very significant.
```
3873.2733: [HammerOfWrath,CrusaderStrike,Judgement,Consecration,DivineStorm,HolyWrath,Exorcism]
3873.0289: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,Consecration,Exorcism,HolyWrath]
3872.8424: [HammerOfWrath,Judgement,DivineStorm,Consecration,CrusaderStrike,HolyWrath,Exorcism]
3870.6628: [HammerOfWrath,Judgement,Consecration,DivineStorm,CrusaderStrike,HolyWrath,Exorcism]
3868.5641: [CrusaderStrike,HammerOfWrath,Judgement,Consecration,DivineStorm,HolyWrath,Exorcism]
3866.1819: [Judgement,CrusaderStrike,DivineStorm,Consecration,HammerOfWrath,Exorcism,HolyWrath]
3865.3016: [HammerOfWrath,CrusaderStrike,Judgement,Consecration,Exorcism,DivineStorm,HolyWrath]
3864.3593: [CrusaderStrike,Judgement,Consecration,DivineStorm,HammerOfWrath,HolyWrath,Exorcism]
3863.9509: [HammerOfWrath,Judgement,CrusaderStrike,Exorcism,DivineStorm,Consecration,HolyWrath]
3862.4589: [HammerOfWrath,CrusaderStrike,Judgement,Consecration,DivineStorm,Exorcism,HolyWrath]
3859.8928: [Judgement,CrusaderStrike,DivineStorm,HammerOfWrath,Consecration,Exorcism,HolyWrath]
3859.8392: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,HolyWrath,Exorcism,Consecration]
3858.0333: [Judgement,HammerOfWrath,CrusaderStrike,DivineStorm,Consecration,Exorcism,HolyWrath]
3857.8703: [Judgement,HammerOfWrath,Consecration,DivineStorm,CrusaderStrike,HolyWrath,Exorcism]
3857.6601: [Judgement,CrusaderStrike,HammerOfWrath,DivineStorm,Consecration,Exorcism,HolyWrath]
3855.0922: [CrusaderStrike,Judgement,Consecration,HammerOfWrath,DivineStorm,HolyWrath,Exorcism]
3854.9753: [Judgement,Consecration,HammerOfWrath,DivineStorm,CrusaderStrike,HolyWrath,Exorcism]
3854.7317: [Judgement,CrusaderStrike,DivineStorm,Consecration,Exorcism,HammerOfWrath,HolyWrath]
```
Let's look at the average ability rankings and how stable they are.
```
- HoW  : 1,1,1,1,2,5,1,5,1,1,4,1,2,2,3,4,3,6
- JoW  : 3,2,2,2,3,1,3,2,2,3,1,2,1,1,1,2,1,1
- CS   : 1,3,5,5,1,2,2,1,3,2,2,3,3,5,2,1,5,2
- DS   : 5,4,3,4,5,3,6,4,5,5,3,4,4,4,4,5,4,3
- Cons : 4,5,4,3,4,4,4,3,6,4,5,7,5,3,5,3,2,4
- Exo  : 7,6,7,7,7,6,5,7,4,6,6,6,6,7,6,7,7,5
- HW   : 6,7,6,6,6,7,7,6,7,7,7,5,7,6,7,6,6,7
```
Average ranks and std deviations:
```
JoW   - 1.83 +/- 0.76
HoW   - 2.44 +/- 1.64
CS    - 2.67 +/- 1.41
DS    - 4.17 +/- 0.83
Cons  - 4.17 +/- 1.17
Exo   - 6.22 +/- 0.85
HW    - 6.44 +/- 0.60
```

So it seems like the sim places JoW/HoW/CS in a league of their own with regards to prio most of the time.
DS and Consecrate slot in nicely below that, with Exo and HW propping up the bottom of the table.

But... the effects can be quite marginal.

# Using these to develop a standard prio
So with that in mind, I think the following are worth adopting for a "standard rotation":

### Keep HoW at #1
Hammer of Wrath is well represented as top ranking among the very best prios.

There is, imo, no reason to not ever prio HoW as your top ability. It's your hardest hitting ability by some way post bug-fix, and its cooldown is relatively short at 6s; even shorter while wings is up if you glyph AW.

The effects of cooldown clash are going to be relatively low over a short execute phase where you are saturated with abilities, so you only really care about maximising the number of high-impact casts before the fight ends in an execute phase.

### Keep JoW at #2
2. Even accounting for us constraining Judgement to the top 3 ranks due to mana concerns, it is still very very well represented at the top 2 spots. It hits extremely hard due to its high base damage and your Fanatacism talent boosting its base dps. Hoever, the tradeoff between CS and judge appears to not amount to a whole lot. If you prio CS higher, it's very short 4s cooldown probably gives you slightly more casts on average, which can overcome the higher damage Judgement.

However, given when you approach a boss, you can cast JoW at range as you close in. For some bosses you rocketboot in so the effect is marginal, but on many fights you want to save boots to cheese some mechanic. You get only one cast of them on any but the absolute longest of multi-phase fights.

As such, I think having JoW fixed at #2 will result in your opening sequence of casts naturally lend itself to syncing up with the prio over the majority of the fight.

### Keep CS at #3
In most setups, the sim and Sulis' tool show the value of keeping your CS on its short 4s cooldown. It's definitely better than any alternatives for this slot, especially when the Libram buff is taken into account.

### Consecrate and DS at #4/#5
There appears to be very little difference between Consecrate and DS over the prios. Over the top prios, they have exactly the same average position.

There is, however, something to be said in real-life terms for having consecrate be on a higher priority:
1 - If you cast it first on your opener, it is already doing full consecrate damage. DS's damage is partially tied up in a SoV proc, which on opener is still stacking. By delaying DS a little, you'll get another melee off to stack vengeance before you cast your first DS for a bit more SoV damage, usually 3 stacks vs 2 stacks.
2 - When you get into execute phase, you want to avoid a situation where you're in the last few GCDs with only consecrate left to cast, when you're only going to get a few ticks off before the fight ends. Having it as a higher prio keeps it on cooldown in execute phase more often, so you're more likely to have a high impact instant-damage ability like DS or Exo to use as an alternative.

### Exo and HW at #6/#7
With these abilities, it ultimately just comes down to their extremely long cooldowns yielding a very marginal increase to Effective Cooldown if you prio them below everything else.

In execute, just be aware that Exo hits harder than a CS, so if you have the choice of one or another before the boss will die, cast the Exo.



# Appendix: Top 100 sequences

3873.2733: [HammerOfWrath,CrusaderStrike,Judgement,Consecration,DivineStorm,HolyWrath,Exorcism]
3873.0289: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,Consecration,Exorcism,HolyWrath]
3872.8424: [HammerOfWrath,Judgement,DivineStorm,Consecration,CrusaderStrike,HolyWrath,Exorcism]
3870.6628: [HammerOfWrath,Judgement,Consecration,DivineStorm,CrusaderStrike,HolyWrath,Exorcism]
3868.5641: [CrusaderStrike,HammerOfWrath,Judgement,Consecration,DivineStorm,HolyWrath,Exorcism]
3866.1819: [Judgement,CrusaderStrike,DivineStorm,Consecration,HammerOfWrath,Exorcism,HolyWrath]
3865.3016: [HammerOfWrath,CrusaderStrike,Judgement,Consecration,Exorcism,DivineStorm,HolyWrath]
3864.3593: [CrusaderStrike,Judgement,Consecration,DivineStorm,HammerOfWrath,HolyWrath,Exorcism]
3863.9509: [HammerOfWrath,Judgement,CrusaderStrike,Exorcism,DivineStorm,Consecration,HolyWrath]
3862.4589: [HammerOfWrath,CrusaderStrike,Judgement,Consecration,DivineStorm,Exorcism,HolyWrath]
3859.8928: [Judgement,CrusaderStrike,DivineStorm,HammerOfWrath,Consecration,Exorcism,HolyWrath]
3859.8392: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,HolyWrath,Exorcism,Consecration]
3859.6425: [CrusaderStrike,HammerOfWrath,Consecration,Judgement,DivineStorm,Exorcism,HolyWrath]
3858.0333: [Judgement,HammerOfWrath,CrusaderStrike,DivineStorm,Consecration,Exorcism,HolyWrath]
3857.8703: [Judgement,HammerOfWrath,Consecration,DivineStorm,CrusaderStrike,HolyWrath,Exorcism]
3857.6601: [Judgement,CrusaderStrike,HammerOfWrath,DivineStorm,Consecration,Exorcism,HolyWrath]
3856.8004: [HammerOfWrath,CrusaderStrike,Consecration,Judgement,DivineStorm,Exorcism,HolyWrath]
3855.0922: [CrusaderStrike,Judgement,Consecration,HammerOfWrath,DivineStorm,HolyWrath,Exorcism]
3854.9753: [Judgement,Consecration,HammerOfWrath,DivineStorm,CrusaderStrike,HolyWrath,Exorcism]
3854.7317: [Judgement,CrusaderStrike,DivineStorm,Consecration,Exorcism,HammerOfWrath,HolyWrath]
3853.6674: [CrusaderStrike,Consecration,HammerOfWrath,Judgement,DivineStorm,Exorcism,HolyWrath]
3852.9753: [Judgement,Consecration,DivineStorm,CrusaderStrike,HolyWrath,HammerOfWrath,Exorcism]
3852.6930: [Judgement,HammerOfWrath,DivineStorm,Consecration,CrusaderStrike,HolyWrath,Exorcism]
3852.5761: [HammerOfWrath,Judgement,DivineStorm,CrusaderStrike,Consecration,Exorcism,HolyWrath]
3852.2867: [CrusaderStrike,Judgement,Consecration,DivineStorm,HolyWrath,Exorcism,HammerOfWrath]
3852.2852: [Judgement,DivineStorm,HammerOfWrath,Consecration,CrusaderStrike,HolyWrath,Exorcism]
3851.4055: [Judgement,Consecration,DivineStorm,HammerOfWrath,CrusaderStrike,HolyWrath,Exorcism]
3851.0597: [CrusaderStrike,HammerOfWrath,Judgement,Consecration,Exorcism,DivineStorm,HolyWrath]
3850.8453: [Judgement,CrusaderStrike,DivineStorm,Consecration,Exorcism,HolyWrath,HammerOfWrath]
3850.6663: [HammerOfWrath,CrusaderStrike,Judgement,Consecration,HolyWrath,Exorcism,DivineStorm]
3850.6402: [Judgement,DivineStorm,Consecration,CrusaderStrike,HolyWrath,HammerOfWrath,Exorcism]
3850.5329: [HammerOfWrath,DivineStorm,Judgement,Consecration,CrusaderStrike,Exorcism,HolyWrath]
3849.7803: [Judgement,DivineStorm,Consecration,CrusaderStrike,HammerOfWrath,HolyWrath,Exorcism]
3849.6766: [Judgement,Consecration,DivineStorm,CrusaderStrike,HammerOfWrath,HolyWrath,Exorcism]
3849.6624: [Judgement,DivineStorm,Consecration,HammerOfWrath,CrusaderStrike,HolyWrath,Exorcism]
3847.9456: [CrusaderStrike,HammerOfWrath,Judgement,Consecration,DivineStorm,Exorcism,HolyWrath]
3847.8688: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,Exorcism,Consecration,HolyWrath]
3847.8584: [Judgement,CrusaderStrike,Consecration,HammerOfWrath,HolyWrath,Exorcism,DivineStorm]
3847.2520: [Judgement,CrusaderStrike,Consecration,HolyWrath,HammerOfWrath,Exorcism,DivineStorm]
3847.0586: [HammerOfWrath,Judgement,CrusaderStrike,Consecration,HolyWrath,Exorcism,DivineStorm]
3846.5050: [CrusaderStrike,Judgement,Consecration,HammerOfWrath,HolyWrath,Exorcism,DivineStorm]
3846.3164: [CrusaderStrike,Judgement,Consecration,HolyWrath,HammerOfWrath,Exorcism,DivineStorm]
3846.2911: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,Consecration,HolyWrath,Exorcism]
3845.9125: [HammerOfWrath,CrusaderStrike,Judgement,DivineStorm,Consecration,HolyWrath,Exorcism]
3845.8758: [HammerOfWrath,Judgement,Consecration,CrusaderStrike,DivineStorm,HolyWrath,Exorcism]
3845.6676: [Consecration,HammerOfWrath,Judgement,DivineStorm,CrusaderStrike,Exorcism,HolyWrath]
3845.6541: [CrusaderStrike,HammerOfWrath,Judgement,Consecration,HolyWrath,Exorcism,DivineStorm]
3845.2007: [HammerOfWrath,CrusaderStrike,Judgement,HolyWrath,Consecration,DivineStorm,Exorcism]
3845.0907: [HammerOfWrath,CrusaderStrike,Judgement,HolyWrath,DivineStorm,Exorcism,Consecration]
3844.9269: [HammerOfWrath,Judgement,Consecration,CrusaderStrike,HolyWrath,DivineStorm,Exorcism]
3844.4363: [HammerOfWrath,CrusaderStrike,Judgement,DivineStorm,HolyWrath,Consecration,Exorcism]
3844.4106: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,Exorcism,HolyWrath,Consecration]
3844.3567: [HammerOfWrath,Consecration,Judgement,DivineStorm,CrusaderStrike,Exorcism,HolyWrath]
3844.2349: [CrusaderStrike,Judgement,HammerOfWrath,Consecration,DivineStorm,HolyWrath,Exorcism]
3843.8361: [HammerOfWrath,Judgement,DivineStorm,CrusaderStrike,Consecration,HolyWrath,Exorcism]
3843.5095: [HammerOfWrath,Judgement,CrusaderStrike,HolyWrath,DivineStorm,Consecration,Exorcism]
3842.2050: [CrusaderStrike,HammerOfWrath,Judgement,DivineStorm,Consecration,HolyWrath,Exorcism]
3841.7460: [Judgement,CrusaderStrike,Exorcism,DivineStorm,Consecration,HammerOfWrath,HolyWrath]
3841.7404: [CrusaderStrike,HammerOfWrath,Exorcism,Judgement,Consecration,HolyWrath,DivineStorm]
3841.7139: [HammerOfWrath,Judgement,CrusaderStrike,DivineStorm,HolyWrath,Consecration,Exorcism]
3840.8536: [CrusaderStrike,Judgement,Consecration,HammerOfWrath,Exorcism,DivineStorm,HolyWrath]
3840.7815: [DivineStorm,HammerOfWrath,Judgement,Consecration,CrusaderStrike,Exorcism,HolyWrath]
3839.4351: [Judgement,CrusaderStrike,DivineStorm,HolyWrath,Exorcism,HammerOfWrath,Consecration]
3839.3420: [CrusaderStrike,Judgement,DivineStorm,Consecration,HammerOfWrath,HolyWrath,Exorcism]
3839.3241: [HammerOfWrath,CrusaderStrike,Exorcism,Judgement,Consecration,HolyWrath,DivineStorm]
3838.4975: [CrusaderStrike,Judgement,DivineStorm,Consecration,HolyWrath,HammerOfWrath,Exorcism]
3838.2944: [CrusaderStrike,Judgement,Consecration,Exorcism,DivineStorm,HammerOfWrath,HolyWrath]
3838.1866: [HammerOfWrath,CrusaderStrike,Judgement,Exorcism,Consecration,DivineStorm,HolyWrath]
3838.0518: [HammerOfWrath,CrusaderStrike,Judgement,HolyWrath,DivineStorm,Consecration,Exorcism]
3837.9412: [HammerOfWrath,CrusaderStrike,Judgement,DivineStorm,HolyWrath,Exorcism,Consecration]
3837.9241: [Judgement,CrusaderStrike,DivineStorm,HolyWrath,Exorcism,Consecration,HammerOfWrath]
3837.8374: [CrusaderStrike,HammerOfWrath,Judgement,DivineStorm,HolyWrath,Consecration,Exorcism]
3837.8044: [HammerOfWrath,Judgement,CrusaderStrike,Consecration,HolyWrath,DivineStorm,Exorcism]
3837.7562: [Judgement,CrusaderStrike,DivineStorm,HammerOfWrath,HolyWrath,Exorcism,Consecration]
3837.7257: [HammerOfWrath,Judgement,DivineStorm,CrusaderStrike,HolyWrath,Exorcism,Consecration]
3837.6296: [Judgement,CrusaderStrike,DivineStorm,HolyWrath,HammerOfWrath,Exorcism,Consecration]
3837.5452: [CrusaderStrike,Judgement,Consecration,HammerOfWrath,DivineStorm,Exorcism,HolyWrath]
3837.3177: [HammerOfWrath,Judgement,CrusaderStrike,Consecration,DivineStorm,HolyWrath,Exorcism]
3837.2905: [HammerOfWrath,CrusaderStrike,Exorcism,Judgement,DivineStorm,Consecration,HolyWrath]
3837.1390: [HammerOfWrath,CrusaderStrike,Judgement,Exorcism,DivineStorm,Consecration,HolyWrath]
3837.0807: [Judgement,HammerOfWrath,Consecration,CrusaderStrike,DivineStorm,HolyWrath,Exorcism]
3836.7900: [CrusaderStrike,Judgement,DivineStorm,HammerOfWrath,Consecration,HolyWrath,Exorcism]
3836.7520: [HammerOfWrath,DivineStorm,Judgement,Consecration,CrusaderStrike,HolyWrath,Exorcism]
3836.6567: [CrusaderStrike,HammerOfWrath,Exorcism,Judgement,HolyWrath,Consecration,DivineStorm]
3836.6300: [HammerOfWrath,Judgement,CrusaderStrike,HolyWrath,Consecration,DivineStorm,Exorcism]
3836.5271: [Judgement,CrusaderStrike,Consecration,Exorcism,DivineStorm,HammerOfWrath,HolyWrath]
3836.1415: [HammerOfWrath,Judgement,CrusaderStrike,Exorcism,Consecration,DivineStorm,HolyWrath]
3836.0431: [HammerOfWrath,CrusaderStrike,Exorcism,Judgement,Consecration,DivineStorm,HolyWrath]
3836.0080: [HammerOfWrath,Judgement,CrusaderStrike,HolyWrath,DivineStorm,Exorcism,Consecration]
3835.9210: [Judgement,CrusaderStrike,Consecration,HolyWrath,Exorcism,HammerOfWrath,DivineStorm]
3835.7829: [CrusaderStrike,Exorcism,HammerOfWrath,Judgement,Consecration,HolyWrath,DivineStorm]
3835.7295: [CrusaderStrike,DivineStorm,HammerOfWrath,Consecration,Exorcism,Judgement,HolyWrath]
3835.6969: [CrusaderStrike,Judgement,Consecration,DivineStorm,HammerOfWrath,Exorcism,HolyWrath]
3835.6225: [Judgement,CrusaderStrike,Consecration,DivineStorm,Exorcism,HammerOfWrath,HolyWrath]
3834.9466: [CrusaderStrike,Judgement,Consecration,Exorcism,HammerOfWrath,DivineStorm,HolyWrath]
3834.7812: [CrusaderStrike,Judgement,Consecration,HolyWrath,Exorcism,HammerOfWrath,DivineStorm]
3834.5108: [CrusaderStrike,Judgement,DivineStorm,HolyWrath,Consecration,HammerOfWrath,Exorcism]
3834.4353: [HammerOfWrath,CrusaderStrike,Exorcism,Judgement,HolyWrath,Consecration,DivineStorm]
3834.2545: [Judgement,Exorcism,CrusaderStrike,DivineStorm,Consecration,HammerOfWrath,HolyWrath]
3834.1183: [Judgement,CrusaderStrike,Consecration,HolyWrath,Exorcism,DivineStorm,HammerOfWrath]
3834.0412: [CrusaderStrike,HammerOfWrath,Judgement,HolyWrath,Consecration,DivineStorm,Exorcism]