import datetime
import re

regex = re.compile(r"\[(\d*)-(\d*)-(\d*) (\d*):(\d*)\] (.*)")
events = {}
with open("4.txt", "r") as infile:
	for line in infile:
		matched = regex.match(line.strip())
		year, month, day, hour, minute, note = \
			int(matched[1]), int(matched[2]), int(matched[3]), int(matched[4]), int(matched[5]), matched[6]
		#print(year, month, day, hour, minute, note)
		timestamp = datetime.datetime(year, month, day, hour, minute)
		events[timestamp] = note
		
guard_regex = re.compile(r".*#(\d*)")
guard_history = {}
guard_sleep_total = {}
sleep_time = 0
for event_time in sorted(events.keys()):
	note = events[event_time]
	guard_match = guard_regex.search(note)
	if guard_match:
		guard_id = int(guard_match[1])
		#print(guard_id)
	elif "falls asleep" in note:
		sleep_time = event_time.minute
		#print(f"sleep: {sleep_time}")
	elif "wakes up" in note:
		wake_time = event_time.minute
		sleep_range = range(sleep_time, wake_time)
		#print(f"wake= {wake_time}")
		
		if guard_id in guard_history:
			guard_history[guard_id].append(sleep_range)
		else:
			guard_history[guard_id] = [sleep_range]
		guard_sleep_total[guard_id] = guard_sleep_total.get(guard_id, 0) + len(sleep_range)
	else:
		raise ValueError(f"Invalid line: {note}")
			
most_id = None
max_slept = 0
max_slept_minute = None
for guard_id in guard_history.keys():
	sleep_history = [0] * 60
	for this_range in guard_history[guard_id]:
		for sleep_minute in this_range:
			sleep_history[sleep_minute] += 1
	max_minute = sleep_history.index(max(sleep_history))
	print(f"Guard: {guard_id}, most slept {max(sleep_history)} ({sleep_history[max_minute]}), minute: {max_minute}")
	print(sleep_history)
	if sleep_history[max_minute] > max_slept:
		max_slept = sleep_history[max_minute]
		most_id = guard_id
		max_slept_minute = max_minute
print(f"Guard {most_id} most asleep at minute {max_slept_minute}: {max_slept}")
print(most_id * max_slept_minute)
