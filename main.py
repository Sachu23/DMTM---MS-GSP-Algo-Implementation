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
                    counter = j+1
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


def init_pass(M,CountMap,seqCount,MIS,LMap):
    counter = 0
    for i in M:
        support = float(CountMap[i])/float(seqCount)
        if(support < MIS[i]):
            counter = counter + 1
        else:
            break

    checkMIS = MIS[M[counter]]
    LMap[M[counter]] = CountMap[M[counter]]

    for i in M[counter+1:]:
        support = float(CountMap[i])/float(seqCount)
        if(support>=checkMIS):
            LMap[i] = CountMap[i]

    add_to_L = [[k,v] for k, v in LMap.items()]
    return add_to_L


def ms_gsp(S, MIS, SDC):
    M = []
    L = []
    CountMap = {}
    LMap = {}
    F1 = []
    F = []
    seqCount = len(S)

    for i in sorted(MIS, key=MIS.get, reverse=False):
        M.append(i)

    for i in M:
        count = 0
        for row in S:
            for elem in row:
                if (elem.count(i)):
                    count = count + 1
                    CountMap[i] = count
                    break

    for i in M:
        if i not in CountMap:
            M.remove(i)

    L = init_pass(M, CountMap, seqCount, MIS, LMap)

    for i in range(len(L)):
        support = float(L[i][1]) / seqCount
        if (support >= MIS[L[i][0]]):
            F1.append(L[i][0])

    output_file = open("Output_MS-GSP_ORG.txt", "w")
    output_file.write("The number of length 1 sequential pattern is " + str(len(F1)) + "\n")
    for f in F1:
        print_s = "Pattern : <{" + str(f) + "}"
        print_s += ">"
        print_s += ": Count = " + str(CountMap[f])
        output_file.write(print_s + "\n")

    k = 2

    Ck = []

    while (True):
        # print("K", k)
        if k == 2:
            Ck = level_2(L, MIS, seqCount, SDC)
        else:
            Ck = MScandidateGen(Fk, M, CountMap, SDC, MIS)

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
            if SupCount[c] / seqCount >= MinMIS(Ck[c], MIS):
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