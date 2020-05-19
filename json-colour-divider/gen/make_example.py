import json
import random

output_name = "../input.json"

colours = [
    ("red", 0.4),
    ("blue", 0.4),
    ("green", 0.1),
    ("purple", 0.05),
    ("orange", 0.05)
]

if __name__ == "__main__":
    output = []

    for i in range(1000):
        r = random.random()
        accum = 0

        for this_colour, p in colours:
            accum += p

            if r < accum:
                colour = this_colour
                break

        output.append({
            "colour": colour,
            "index": i
        })

    with open(output_name, "w") as out_file: 
        json.dump(output, out_file, indent=4)
