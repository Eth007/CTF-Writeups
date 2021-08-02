# toobeetootee - 464 pts, 7 solves
> Oh no! the infamous popbob hacked into my Minetest server, griefed my house, and tampered with the flag! Luckily, I was running a network capture at the time. Can you help me rollback the damage?
> 
> toobeetootee.pcap world.zip

`toobeetootee` was a forensics challenge in UIUCTF 2021, where I played with `TeamlessCTF`, getting second blood on this challenge and 12th place overall. Let's dive into the challenge.

We are presented with a PCAP file and a zip file containing the minetest world. Upon inspection, we find that the world contains a fake flag written using Minetest blocks (pine wood blocks, to be exact :P).

![Fake flag](fake_flag.png)
