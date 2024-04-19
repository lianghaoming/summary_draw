import sys
import statistics
import matplotlib.pyplot

import sys
import statistics
import matplotlib.pyplot


def parse(filename):
    with open(filename, "r") as f:
        headings = None
        data = {}
        lengths = []
        is_header_found = False  # Flag to indicate if the actual headers have been set
        for line in f:
            stripped_line = line.strip()
            print(f"Reading line: {stripped_line}")
            if not stripped_line:
                continue  # Skip empty lines
            if "MEANS" in stripped_line or "STDEVS" in stripped_line:
                is_header_found = False  # Reset on section headers
                continue
            if not is_header_found:
                headings = stripped_line.split('\t')
                print(f"Headings set to: {headings}")
                is_header_found = True
                continue
            row = stripped_line.split('\t')
            if row and len(row) == len(headings):
                generations = row[0]
                if generations not in lengths:
                    lengths.append(generations)
                for i in range(1, len(row)):
                    try:
                        cost = float(row[i])
                        head = headings[i]
                        if (generations, head) in data:
                            data[(generations, head)].append(cost)
                        else:
                            data[(generations, head)] = [cost]
                    except ValueError:
                        print(f"Warning: Skipping invalid data '{row[i]}' in column {headings[i]}")
            else:
                print(f"Warning: Skipping line with unexpected number of columns: {line}")
                print(f"Expected {len(headings)} columns, but found {len(row)} columns.")
        return data, headings, lengths


if __name__ == "__main__":
    datafile = 'system-stats.txt' # Path to the input data file
    figureFilename = datafile[:-4] + ".svg"
    epsFilename = datafile[:-4] + ".eps"
    data, headings, lengths = parse(datafile)

    means = {headings[i]: [] for i in range(1, len(headings))}
    devs = {headings[i]: [] for i in range(1, len(headings))}
    for gens in lengths:
        for i in range(1, len(headings)):
            head = headings[i]

            means[head].append(statistics.mean(data[(gens, head)]))
            devs[head].append(statistics.stdev(data[(gens, head)]))

    print("MEANS")
    print(headings[1], end="")
    for i in range(2, len(headings)):
        print("\t" + headings[i], end="")
    print()
    for i, gens in enumerate(lengths):
        print(gens, end="")
        for j in range(1, len(headings)):
            head = headings[j]
            print("\t{0:.2f}".format(means[head][i]), end="")
        print()
    print()
    print("STDEVS")
    print(headings[1], end="")
    for i in range(2, len(headings)):
        print("\t" + headings[i], end="")
    print()
    for i, gens in enumerate(lengths):
        print(gens, end="")
        for j in range(1, len(headings)):
            head = headings[j]

            print("\t{0:.2f}".format(devs[head][i]), end="")
        print()

    w = 2.98
    h = w
    matplotlib.pyplot.rc('font', size=8)
    matplotlib.pyplot.rc('text', usetex=True)
    fig, ax = matplotlib.pyplot.subplots(figsize=(w, h), constrained_layout=True)
    matplotlib.pyplot.xlabel('number of generations (log scale)')
    matplotlib.pyplot.ylabel('average solution cost')
    for i in range(1, len(headings)):
        line, = ax.plot(lengths,
                        means[headings[i]],
                        # styles[i],
                        label=headings[i])
    ax.legend()
    matplotlib.pyplot.savefig(figureFilename)
    matplotlib.pyplot.savefig(epsFilename)