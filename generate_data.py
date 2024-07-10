import random
from datetime import datetime, timedelta
import pytz

# Function to generate random timestamps for the year 2024
def generate_random_timestamp(year):
    start_date = datetime(year, 1, 1, 0, 0, 0)
    end_date = datetime(year + 1, 1, 1, 0, 0, 0)
    delta = end_date - start_date
    random_second = random.randint(0, int(delta.total_seconds() - 1))
    random_date = start_date + timedelta(seconds=random_second)
    
    timezone = pytz.FixedOffset(60)  # UTC+01:00
    random_date = random_date.replace(tzinfo=pytz.utc).astimezone(timezone)
    
    return random_date.strftime('%Y-%m-%d %H:%M:%S%z')

# Generate 383 timestamps for the year 2024
timestamps = [generate_random_timestamp(2024) for _ in range(383)]

# Save the generated timestamps to a file
with open('timestamps.txt', 'w') as file:
    for timestamp in timestamps:
        file.write(timestamp + '\n')

print("Original timestamps have been saved to 'timestamps.txt'.")

# Read the original timestamps from the file
with open('timestamps.txt', 'r') as file:
    original_timestamps = file.readlines()

# Adjust each timestamp to be one day before
adjusted_timestamps = []
for timestamp in original_timestamps:
    timestamp = timestamp.strip()  # Remove any leading/trailing whitespace
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S%z')
    new_dt = dt - timedelta(days=1)
    adjusted_timestamps.append(new_dt.strftime('%Y-%m-%d %H:%M:%S%z'))

# Save the adjusted timestamps to a different file
with open('adjusted_timestamps.txt', 'w') as file:
    for timestamp in adjusted_timestamps:
        file.write(timestamp + '\n')

print("Adjusted timestamps have been saved to 'adjusted_timestamps.txt'.")
