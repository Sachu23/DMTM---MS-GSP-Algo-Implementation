import math
from read_inputs import read_seq_file, read_param_file
from candidate_generation import level_2, MScandidateGen


def MinMIS(Ck, MIS):
    minMIS = math.inf
    for i in Ck:
        for j in i:
            if MIS[j] < minMIS:
                minMIS = MIS[j]
    return minMIS


def Subset(Ck, s):
    if len(list(set(Ck))) != len(Ck):
        return False
    for i in Ck:
        if i not in s:
            return False
    return True


def Sub(Ck, s):
    m = {}
    counter = 0
    for i in Ck:
        isThere = False
        j = counter
        while j < len(s):
            if j in m:
                continue
            else:
                if Subset(i, s[j]):
                    m[j] = True
                    isThere = True
                    counter = j + 1
                    break
            j += 1
        if not isThere:
            return False
    return True


def remove_duplicates(d):
    final = []
    for n in d:
        if n not in final:
            final.append(n)
    return final


def init_pass(M, CountMap, seq_count, MIS, LMap):
    ctr = 0
    for i in M:
        support = float(CountMap[i]) / float(seq_count)
        if (support < MIS[i]):
            ctr += 1
        else:
            break
    # changes made below to list comprehension for a more explicit loop

    checkMIS = MIS[M[ctr]]
    LMap = {M[ctr]: CountMap[M[ctr]]}

    # Iterate over M to find frequent items
    for i in M[ctr + 1:]:
        support = CountMap[i] / seq_count #float type conversion not needed
        if support >= checkMIS:
            LMap[i] = CountMap[i]

    # Convert LMap to a list and return
    add_to_L = [[k, v] for k, v in LMap.items()]
    return add_to_L


def ms_gsp(S, MIS, SDC):
    M = list()  # Sorted MIS values
    M = [x for x in sorted(MIS, key=MIS.get)]

    count_map = dict()
    for i in M:
        count = 0
        for row in S:
            if any(i in elem for elem in row):
                count += 1
        if count:
            count_map[i] = count

    new_M = [i for i in M if i in count_map]
    M.clear()
    M.extend(new_M)

    seq_count = len(S)
    LMap = dict()

    L = init_pass(M, count_map, seq_count, MIS, LMap)

    F1 = list()
    for i in range(len(L)):
        support = float(L[i][1]) / seq_count
        if support >= MIS[L[i][0]]:
            F1.append(L[i][0])

    output_file = open("Output_MS-GSP_ORG.txt", "w")
    output_file.write("The number of length 1 sequential pattern is " + str(len(F1)) + "\n")
    for f in F1:
        print_s = "Pattern : <{" + str(f) + "}"
        print_s += ">"
        print_s += ": Count = " + str(count_map[f])
        output_file.write(print_s + "\n")

    k = 2
    while (True):
        # print("K", k)
        if k == 2:
            Ck = level_2(L, MIS, seq_count, SDC)
        else:
            Ck = MScandidateGen(Fk, M, count_map, SDC, MIS)

        # print("C", Ck)
        # print("Length of C", len(Ck))
        SupCount = [0] * len(Ck)
        for c in range(len(Ck)):
            temp_count = 0
            for s in S:
                if Sub(Ck[c], s):
                    temp_count += 1
            SupCount[c] = temp_count

        # print("Count",SupCount)
        Fk = []
        Fk_withcount = []
        for c in range(len(Ck)):
            if SupCount[c] / seq_count >= MinMIS(Ck[c], MIS):
                Fk.append(Ck[c])
                Fk_withcount.append([Ck[c], SupCount[c]])
        # print("K", k)
        # print("Support Count", SupCount)
        # F.extend(Fk)
        # print("Fk", Fk)
        # print("Length of Fk", len(Fk))
        Fk = remove_duplicates(Fk)
        Fk_withcount = remove_duplicates(Fk_withcount)

        if (len(Fk) == 0):
            break

        output_file.write("The number of length: " + str(k) + " sequential pattern is " + str(len(Fk)) + "\n")
        for f in Fk_withcount:
            print_s = "Pattern : <"
            for s in f[0]:
                print_s += "{"
                for i in s:
                    print_s += str(i) + ","
                # print_s += ","
                print_s = print_s[:-1]
                print_s += "}"
            print_s += ">:Count = " + str(f[1])
            output_file.write(print_s + "\n")
        k += 1


if __name__ == '__main__':
    seq_list = read_seq_file()
    min_seq_dict, sdc_val = read_param_file()
    ms_gsp(seq_list, min_seq_dict, sdc_val)
