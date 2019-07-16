import sc2reader
from pathlib import Path
from collections import Counter

abilities = {"Terran": Counter(), "Zerg": Counter(), "Protoss": Counter()}
races = Counter()

total = len(list(Path("replays").glob("**/*.SC2Replay")))
print(f"parsing {total} replays...")
for i,replayname in enumerate(Path("replays").glob("**/*.SC2Replay")):

	# I've had some replays fail to load, error message said "Stet"
	# I assume it meant Stetmann. If you're not loading coop games it's fine.
	replay = sc2reader.load_replay(replayname.open("rb"))

	# Some of the replays in tournament packs are unloadable for some reason.
	# They also cannot be viewed in the normal client.
	# In particular, these series refuse to load:
	# WCS Summer, Knockout Round 1, Vanya - MODEUS
	# WCS Summer, Knockout Round 2, Vanya - BuRning
	unrecognized = False
	for x in replay.players:
		if x.play_race not in ["Terran", "Zerg", "Protoss"]:
			unrecognized = True
			print("unrecognized race", x, replayname)
	if unrecognized:
		continue

	races.update(x.play_race for x in replay.players if x)
	for ev in replay.game_events:
		if "ability_name" in dir(ev):
			abilities[ev.player.play_race][ev.ability_name] += 1

	print(f"{int(i*100./total)}%")

# json.dump can't output in sorted order, which is nice for manual inspection
for race in ["Protoss", "Terran", "Zerg"]:
	with open(f"{race}.json", "w") as fh:
		fh.write("{\n")
		fh.write(f'"total games": {races[race]},\n')
		f = True
		for k,v in sorted(abilities[race].items(), key=lambda x:-x[1]):
			if f:
				f = False
			else:
				fh.write(",\n")
			fh.write(f'"{k}": {v}')
		fh.write("\n}\n")
