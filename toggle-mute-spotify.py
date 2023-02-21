#!/usr/bin/env python3

import subprocess
import re
import sys

# Run the command and capture its output as a byte string
output_bytes = subprocess.check_output(
	['pactl', 'list', 'sink-inputs']
)

# Convert the byte string to a regular string using UTF-8 encoding
sinks_str = output_bytes.decode('utf-8')

sinks = {}

# Loop through sinks string and convert entries to simple dict
# to look up a sink by its application name.
for s in sinks_str.split('\n\n'):
	app_re = re.search(r'application\.name\s?\=\s?([\"\'\w\d\ ]+)', s)
	id_re = re.search(r'Sink Input #([\w\ \d]+)', s)

	app = app_re.group(1).replace('"', '')
	input_id = id_re.group(1)

	sinks[app] = input_id

# Use the first command line argument to toggle the mute of an app
if len(sys.argv) > 1:
	app = sys.argv[1]

	if app in sinks:
		cmd = subprocess.check_output(
			['pactl', 'set-sink-input-mute', sinks[app], 'toggle']
		)
		print(cmd.decode('utf-8'))
