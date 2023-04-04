import re

payload = '03-14 08:45:58.669  3788  3499 D RAW POSE: x=0.1 y=0.5 z=0.1'

match = re.search(r'RAW POSE: x=(-?\d+\.\d+)\s+y=(-?\d+\.\d+)\s+z=(-?\d+\.\d+)', payload)

if match:
    x = float(match.group(1))
    y = float(match.group(2))
    z = float(match.group(3))
    print(f'x={x}, y={y}, z={z}')
else:
    print('No match found.')
