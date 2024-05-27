from collections import defaultdict

# Simulated data (replace with your actual data structures)
leximpro_entries = {
    "entry1": ["bird1", "bird2"],
    "entry2": ["bird3"]
}

birdom_entries = {
    "bird1": ["annotation1", "annotation2"],
    "bird2": ["annotation3"]
}

# Use a set to store unique birds for each LeximPro entry
bird_counts = defaultdict(set)

# Iterate through LeximPro entries
for entry, birds in leximpro_entries.items():
    # Add birds to the set for the current entry
    for bird in birds:
        bird_counts[entry].add(bird)

# Count the total unique birds
total_unique_birds = sum(len(birds) for birds in bird_counts.values())

# Print the results
print(
    f"Total unique birds associated with LeximPro entries: {total_unique_birds}")
