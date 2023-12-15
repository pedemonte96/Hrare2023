

if __name__ == "__main__":

    print("-----------------------------------------------------------------------")
    print("------------------------------BERN-------------------------------------")
    print("-----------------------------------------------------------------------")

    fileName = "D0StarRho_bern_MH.txt"
    li = []
    with open(fileName, 'r') as file:
        for line in file:
            parts = line.rsplit(',', 1)
            li.append([float(parts[1]), parts[0]])

    for a in sorted(li, key=lambda x: x[0])[:10]:
        print(a)

    print("-----------------------------------------------------------------------")
    print("------------------------------CHEV-------------------------------------")
    print("-----------------------------------------------------------------------")

    fileName = "D0StarRho_chev_MH.txt"
    li = []
    with open(fileName, 'r') as file:
        for line in file:
            parts = line.rsplit(',', 1)
            li.append([float(parts[1]), parts[0]])

    for a in sorted(li, key=lambda x: x[0])[:10]:
        print(a)