"""

TODO

[5:56 AM] Altafen: [5:54 AM] JaKaTaKtv: we just want to know how many times its useful to jump to a spot
ah yes good point - if people use cams for their first 3 but spend a lot of time looking at their 4th we should pick up on that as being a deficiency, not a "oh 3 is good enough for X player"


[5:54 AM] gcask: In the replay, you have the SCameraSaveEvent, which gives you... well, the saved cameras.

make it work for all maps not just Automaton LE

"""

import multiprocessing
import sc2reader
from pathlib import Path
from collections import Counter, defaultdict
def dump(ev):
       for x in dir(ev):
               if x[0] != "_":
                       print(x,"=",repr(getattr(ev,x)))
       print("\n\n")

def mp_process(replayname):
	replay = sc2reader.load_replay(replayname.open("rb"))
	if replay.map_name != "Automaton LE":
		return
	coords = defaultdict(list)
	for ev in replay.game_events:
		if ev.name == "CameraEvent" and not ev.player.is_observer and not ev.player.is_referee:
			coords[ev.player].append((ev.x, ev.y))
	camera_locations = defaultdict(list)
	for player,cams in coords.items():
		for pos1, pos2 in zip(cams, cams[1:]):
			if (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 > 9:
				camera_locations[player].append(pos2)
	return camera_locations

if __name__ == "__main__":
	cam_total = Counter()
	total = len(list(Path("replays").glob("**/*.SC2Replay")))
	print(f"parsing {total} replays...")
	all_locs_x = []
	all_locs_y = []
	with multiprocessing.Pool() as pool:
		for donesofar,cam_thisrun in enumerate(pool.imap_unordered(mp_process, Path("replays").glob("**/*.SC2Replay"))):
			print(f"{donesofar}/{total} = {100*donesofar/total:0.0f}%")
			for plr,cams in (cam_thisrun or {}).items():
				for x,y in cams:
					all_locs_x.append(x)
					all_locs_y.append(y)

	import matplotlib as mpl
	import matplotlib.pyplot as plt
	plt.clf()
	plt.title('cam jumps @ katowice')
	plt.hist2d(all_locs_x, all_locs_y, bins=(64,64), norm=mpl.colors.LogNorm())
	plt.show()
