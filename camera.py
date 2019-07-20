import sc2reader
from pathlib import Path
from collections import Counter, defaultdict
def dump(ev):
       for x in dir(ev):
               if x[0] != "_":
                       print(x,"=",repr(getattr(ev,x)))
       print("\n\n")

total = len(list(Path("replays").glob("**/*.SC2Replay")))
print(f"parsing {total} replays...")
for i,replayname in enumerate(Path("replays").glob("**/*.SC2Replay")):
	replay = sc2reader.load_replay(replayname.open("rb"))
	coords = defaultdict(list)
	for ev in replay.game_events:
		if ev.name == "CameraEvent" and not ev.player.is_observer and not ev.player.is_referee:
			coords[ev.player].append((ev.x, ev.y))
	camera_locations = defaultdict(list)
	for player,cams in coords.items():
		for pos1, pos2 in zip(cams, cams[1:]):
			if (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 > 9:
				camera_locations[player].append(pos2)
	for player,cams in camera_locations.items():
		print(player.name, len(cams))
		print([x[1] for x in Counter(cams).most_common(10)])
		print()
	print("==============================")
