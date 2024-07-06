with open('./part-r-00000.txt', 'r') as infile, open('./part-r-00000.csv', 'w') as outfile:
    for line in infile:
        parts = line.strip().split('\t')  #  tab-separated data
        outfile.write(f'{parts[0]},{parts[1]}\n')
