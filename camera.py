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
		if ev.name == "CameraEvent":
			coords[ev.pid].append((ev.x, ev.y))
	camera_locations = defaultdict(list)
	for pid,cams in coords.items():
		for pos1, pos2 in zip(cams, cams[1:]):
			if (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 > 9:
				camera_locations[pid].append(pos2)
	for pid,cams in camera_locations.items():
		print(replay.players[pid].name, len(cams))
		print(Counter(cams).most_common(10))
		print()
	print("==============================")
