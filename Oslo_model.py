import Pile
import numpy as np
import matplotlib.pyplot as plt

piles = [Pile.Pile(64), Pile.Pile(128), Pile.Pile(256)]

list_of_databases = []
### Preforming analisys
number_of_drives = 5000
for pile in piles:

    # Preforming analysis
    ava_rank, total_sizes = pile.drive_system_multiple_times(number_of_drives) 

    # Postprocessing data
    filename = f"{pile.name}_{number_of_drives}.txt"

    with open(filename, "w", encoding="utf8") as output_file:
        output_file.write("Rank\tAvalanche_size\tCount\tFrequency\n")
        for rank, (size, count) in enumerate(ava_rank, start=1):
            output_file.write(f"{rank}\t{size}\t{count}\t{count/total_sizes:.6f}\n")
    list_of_databases.append(filename)
    print(f"Result saved to {filename}")
