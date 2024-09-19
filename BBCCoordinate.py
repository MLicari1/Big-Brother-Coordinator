def read_picks(filename: str) -> dict[str, list[str]]:
    """
    key: individual
    value: his picks
    """
    with open(filename, 'r') as file:
        rows: list[list[str]] = []
        for line in file:
            rows.append(line.strip().replace(", ", ",").split(","))
        return {row[0]: row[1:] for row in rows}


bigs = read_picks("Responses from Bigs.csv")
littles = read_picks("Responses from Littles.csv")

# big, little, pairing score (0 is best)
imperfect_pairings: list[tuple[str, str, int]] = []

# big-little pairings where each was the other's number one
perfect_pairings: list[tuple[str, str]] = []

# names of individuals who have been processed
littles_paired: set[str] = set()
bigs_paired: set[str] = set()

for big, big_picks in bigs.items():
    for big_rank, little in enumerate(big_picks):
        little_picks = littles[little]
        if big in little_picks and little in big_picks:
            little_rank = little_picks.index(big)
            score = big_rank + little_rank
            if score == 0:
                perfect_pairings.append((big, little))
            else:
                imperfect_pairings.append((big, little, score))

            bigs_paired.add(big)
            littles_paired.add(little)



unpaired_littles = {little for little in littles if little not in littles_paired}
unpaired_bigs = {big for big in bigs if big not in bigs_paired}

loose_pairings = set()


for big in unpaired_bigs:
    for little in unpaired_littles:
        big_picks = bigs[big]
        little_picks = littles[little]
        if little in big_picks or big in little_picks:
            loose_pairings.add((big, little))

orphaned_littles = unpaired_littles - {little for _, little in loose_pairings}



imperfect_pairings.sort(key=lambda x: x[2])

print(
"""
clarification: lower score is better than a higher score...
score is calculated by adding up "preference" position within each others list
"preference" position simply means big choice number + little choice number (-2 since coding is index starts at 0)
This an arbitrary ranking. The decision to make pairs is still up to the Kappa and BBC's discretion. Use this tool as a recommendation only.
if a big or little puts a pick down multiple times, the code will still run and execute but will give some meaningless/ duplicate results
"""
)

print("Perfect pairs - each other's number one picks")
for big, little in perfect_pairings:
    print("\t", big, "-", little)


print("\n\nhad each other on list")
for big, little, score in imperfect_pairings:
    print("\t", score, big, "-", little)

print("\n\nunpaired littles - littles with no list matches", *unpaired_littles, sep="\n\t")
print("\n\nunpaired bigs - bigs with no list matches", *unpaired_bigs, sep="\n\t")

print("\n\nloose pairings of the unpaired - pairs from the lists of unpaired where at least on had the other on their list")
for big, little in loose_pairings:
    print("\t", big, '-', little)

print("\n\nFinal Stand - these littles were no-one's top five :(", "\n\t")
print(*orphaned_littles, sep="\n\t")

