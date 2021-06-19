# BCACraft 2.0

Open up NBT editor, find that it's REALLY SLOW to search for stuff. Then use the command line utility to dump the data, and use grep to search for a barrel. After finding the barrel, there's paper containing flag format, 3 compasses pointing to stuff, 3 tasks, and a closing bracket.

Then I was lazy so I booted up Minecraft to view the world. I enabled commands so that I could teleport to the coordinates in the NBT with the `/tp` command.

The 3 compasses point to signs saying `MINE_DIAAA` and `MOOONNDDSSS!!`, as well as to a pile of glass items. Using a hopper to collect the glass, I found that one of the glass blocks was named `_rj57tf`. Now, it asked for some other things. 

> Find the X position of a pig floating above the height limit. (as an integer)

For this, I grepped for all pigs in the world, then scrolled through their coordinates. There was 1 pig at y coordinate `512`, so I teleported there in-game and found a pig in the sky. Copying down the position and rounding, I found `-584594` as the X coordinate. 

> There's a block of red glazed terracotta somewhere in this world. Find its X position.

Grepping for `terracotta`, I found that there was a chunk with terracotta blocks in it. Multiplying chunk coordinates by 16 to get the in-game coordinates of the chunk, I teleported to the location and recorded the X position, `23485584`. 

> Talk to the only villager in this world to get the last part.

Last step. We grep for `villager` and find the coordinates of the villager. In the NBT data we can see that there's a note on the villager saying `JU689JUf`. (also some trades involving netherite and dirt :eyes:)

Putting all these parts together, we get the flag: `bcactf{MINE_DIAAAMOOONNDDSSS!!_rj57tf-58459423485584JU689JUf}`.
