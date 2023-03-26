import re

# Define pattern for extracting relevant information from log line
pattern = r'(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s+(\d+)\s+(\d+)\s+([A-Z]+)\s+(.+)'

# Open log file for reading
with open('r.txt', 'r') as f:

    # Initialize previous timestamp and offset values
    previous_timestamp = 0
    offset = 0
    print("Reading")

    # Read file line by line
    for line in f:
        # Extract relevant information from log line
        match = re.match(pattern, line)
        if match:
            print("MatchFound)")
            day = int(match.group(1))
            month = int(match.group(2))
            hour = int(match.group(3))
            minute = int(match.group(4))
            second = int(match.group(5))
            millisecond = int(match.group(6))
            process_id = int(match.group(7))
            sub_id = int(match.group(8))
            tag = match.group(9)
            payload = match.group(10)

            # Calculate timestamp
            timestamp = millisecond + second * 1000 + minute * 60 * 1000 + hour * 60 * 60 * 1000 + offset

            # Check if current timestamp is more than 100000 less than previous
            if timestamp < previous_timestamp - 100000:
                offset += 24 * 60 * 60 * 1000
                timestamp += 24 * 60 * 60 * 1000

            # Update previous timestamp to current value
            previous_timestamp = timestamp

            # Do whatever processing you need with the extracted information here
            print(f"Date: {day}-{month}, Timestamp: {timestamp}, Process ID: {process_id}, Sub ID: {sub_id}, Tag: {tag}, Payload: {payload}")

