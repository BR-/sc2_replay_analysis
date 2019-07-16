import sc2reader, techlabreactor
from pathlib import Path
from collections import Counter
from pprint import pprint
def dump(ev):
	for x in dir(ev):
		if x[0] != "_":
			print(x,"=",repr(getattr(ev,x)))
	print("\n\n")

c = {"Terran": Counter(), "Zerg": Counter(), "Protoss": Counter()}
races_games = Counter()
total = len(list(Path("D:/scinput").glob("**/*.SC2Replay")))
print(f"parsing {total} replays...")
for i,replayname in enumerate(Path("D:/scinput").glob("**/*.SC2Replay")):
	#try:
	replay = sc2reader.load_replay(replayname.open("rb"))
	#except:
		#continue
	#if not replay.is_ladder:
		#continue
	races_games.update(x.play_race for x in replay.players if x)
	for x in replay.game_events:
		if "ability_name" in dir(x):
			c[x.player.play_race][x.ability_name] += 1
	print(f"{int(i*100./total)}%")

for race in ["Protoss", "Terran", "Zerg"]:
	with open(f"{race}.json", "w") as fh:
		fh.write("{\n")
		fh.write(f"'total games': {races_games[race]},\n")
		f = True
		for k,v in sorted(c[race].items(), key=lambda x:-x[1]):
			if f:
				f = False
			else:
				fh.write(",\n")
			fh.write(f"'{k}': {v}")
		fh.write("\n}\n")
