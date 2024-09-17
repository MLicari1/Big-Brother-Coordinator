def read_shit(filename):
    with open(filename, 'r') as file:
        data = list(map(lambda x: x.split(','), file.read().split('\n')))
        return {row[0]: row[1:] for row in data}
        

bigs = read_shit(r"BBC Sheet - Results.csv")
littles = read_shit(r"BBC Sheet - Sheet2.csv")
in_eachothers_list = []
one_on_ones = []

littles_paired = set()
bigs_paired = set()

for big, big_picks in bigs.items():
    for big_rating, little in enumerate(big_picks):
        if big in (little_picks := littles[little]) and little in big_picks:
            little_rating = little_picks.index(big)
            score = big_rating + little_rating
            if score == 0:
                one_on_ones.append((big, little))
            else:
                in_eachothers_list.append((big, little, score))
            
            bigs_paired.add(big)
            littles_paired.add(little)



unpaired_littles = {little for little in littles if little not in littles_paired}

unpaired_bigs = {big for big in bigs if big not in bigs_paired}

loose_pairings = set()


for big in unpaired_bigs:
    for little in unpaired_littles:
        if big in littles[little] or little in bigs[big]:
            loose_pairings.add((big, little))

homeless_littles = unpaired_littles - {l for _, l in loose_pairings}


    
in_eachothers_list.sort(key=lambda x: x[2])
8
print(
"""
clarification: lower score is better than a higher score...
score is calculated by adding up "preference" position within each others list
"preference" position simply means big choice number + little choice number (-2 since coding is base 0)
This an arbitrary ranking. The decision to make pairs is still up to the Kappa and BBC's discretion. Use this tool as a recommendation only.
if a big or little puts a pick down multiple times, the code will still run and execute but will give some meaningless/ duplicate results
"""
)

print("One-to-One")
for big, little in one_on_ones:
    print("\t", big, "-", little)


print("\n\nhad each other on list")
for big, little, score in in_eachothers_list:
    print("\t", score, big, "-", little)

print("\n\nunpaired littles - littles with no list matches", *unpaired_littles, sep="\n\t")
print("\n\nunpaired bigs - bigs with no list matches", *unpaired_bigs, sep="\n\t")

print("\n\nloose pairings of the unpaired - pairs from the lists of unpaired where at least on had the other on their list")
for big, little in loose_pairings:
    print("\t", big, '-', little)

print("\n\nFinal Stand - these littles were no-one's top five :(", "\n\t")
print(*homeless_littles, sep="\n\t")

