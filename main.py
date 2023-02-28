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


def generate_F1(M, CountMap, seq_count, MIS):
    L = list()
    min_support = -1
    for item in M:
        item_support = float(CountMap[item]) / float(seq_count)
        if min_support == -1:
            if item_support >= MIS[item]:
                L.append(item)
                min_support = MIS[item]
        else:
            if item_support >= min_support:
                L.append(item)

    return L


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
    L = generate_F1(M, count_map, seq_count, MIS)

    F1 = list()
    for i in L:
        item_support = float(count_map[i]) / float(seq_count)
        if item_support >= MIS[i]:
            F1.append(i)

    output_file.write("**************************************\n")
    output_file = open("Output_MS-GSP_ORG.txt", "w")
    output_file.write("1-Sequences:\n")
    for f in F1:
        print_s = "Pattern : <{" + str(f) + "}"
        print_s += ">"
        output_file.write(print_s + "\n")

    output_file.write("The count is: " + str(len(F1)) + "\n")

    k = 2
    while (True):
        if k == 2:
            Ck = level_2(L, MIS, seq_count, SDC, count_map)
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
        Fk = list()
        for c in range(len(Ck)):
            if SupCount[c] / seq_count >= MinMIS(Ck[c], MIS):
                Fk.append(Ck[c])

        Fk = remove_duplicates(Fk)

        if len(Fk) == 0:
            break

        output_file.write("**************************************\n")
        output_file.write(str(k) + "-Sequences:" + "\n")
        for f in Fk:
            print_s = "Pattern : <"
            for s in f:
                print_s += "{"
                for i in s:
                    print_s += str(i) + ","
                print_s = print_s[:-1]
                print_s += "}"
            print_s += ">"
            output_file.write(print_s + "\n")

        output_file.write("The count is: " + str(len(Fk)) + "\n")
        k += 1


if __name__ == '__main__':
    seq_list = read_seq_file()
    min_seq_dict, sdc_val = read_param_file()
    ms_gsp(seq_list, min_seq_dict, sdc_val)
