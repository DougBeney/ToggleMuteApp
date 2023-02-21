#!/usr/bin/env python3

import subprocess
import re
import sys

# Define the command to run
cmd = ['pactl', 'list', 'sink-inputs']

# Run the command and capture its output as a byte string
output_bytes = subprocess.check_output(cmd)

# Convert the byte string to a regular string using UTF-8 encoding
output_str = output_bytes.decode('utf-8')

sinks = {}

# Print the output
for s in output_str.split('\n\n'):
	app_re = re.search(r'application\.name\s?\=\s?([\"\'\w\d\ ]+)', s)
	id_re = re.search(r'Sink Input #([\w\ \d]+)', s)

	app = app_re.group(1).replace('"', '')
	input_id = id_re.group(1)

	sinks[app] = input_id

if len(sys.argv) > 1:
	app = sys.argv[1]

	if app in sinks:
		cmd = subprocess.check_output(['pactl', 'set-sink-input-mute', sinks[app], 'toggle'])
		print(cmd.decode('utf-8'))
