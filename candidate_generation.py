import copy
from copy import deepcopy

import copy
import math
from copy import deepcopy


# below function need L(list of tuple with (item,count)), MIS(dict{(item:MIS)}), n, sdc
def level_2(L1, MIS, seq_count, sdc, count_map):
    C3 = list()
    for i in range(0, len(L1)):
        C3.append([[L1[i]], [L1[i]]])
        C3.append([[L1[i], L1[i]]])
        if (count_map[L1[i]] / seq_count) >= MIS[L1[i]]:
            for j in range(i + 1, len(L1)):
                if ((count_map[L1[j]] / seq_count) >= MIS[L1[i]]) & (
                        abs(count_map[L1[j]] / seq_count - count_map[L1[i]] / seq_count) <= sdc):
                    if L1[i] < L1[j]:
                        C3.append([[L1[i], L1[j]]])
                    else:
                        C3.append([[L1[j], L1[i]]])
                    C3.append([[L1[i]], [L1[j]]])
                    C3.append([[L1[j]], [L1[i]]])

    return C3


def MScandidateGen(F, M, CountMap, SDC, MIS):
    # F[2] = [[[20, 30]], [[20], [30]], [[20, 70]], [[20], [70]], [[20], [80]], [[30], [30]], [[30, 70]], [[30], [70]], [[30, 80]], [[30], [80]], [[70], [70]], [[70, 80]], [[80], [70]], [[10, 40]], [[10], [40]], [[40], [40]]]
    # F[2] = [[[20, 30, 40]], [[40], [70]]]
    # print(F)
    C = []
    for i in F:
        s1 = i
        first_s1 = i[0][0]
        last_s1 = i[-1][-1]
        for j in F:
            s2 = j
            first_s2 = j[0][0]
            last_s2 = j[-1][-1]
            MIS_least_seq = getMISofSequence(s1, MIS, first_s1)
            # print(s1)
            # print(s2)

            if (MIS[first_s1] < MIS_least_seq):
                if ((removeItem(s1, 1) == removeItem(s2, get_length(s2) - 1)) & (MIS[last_s2] > MIS[first_s1])):
                    if (len(s2[-1]) == 1):
                        c1 = []
                        c1 = s1.copy()
                        c1.append([s2[-1][-1]])
                        C.append(c1)

                        if ((get_length(s1) == 2 & len(s1) == 2) & (MIS[last_s2] > MIS[last_s1])):
                            c2 = []
                            c2 = s1.copy()
                            last_c2 = c2[-1].copy()
                            last_c2.append(s2[-1][-1])
                            # c2 = removeItem(c2,get_length(c2)-1)
                            del (c2[-1])
                            c2.append(last_c2)
                            C.append(c2)

                    elif (((get_length(s1) == 2 & len(s1) == 1) & (MIS[last_s2] > MIS[last_s1])) | (
                            get_length(s1) > 2)):
                        c2 = []
                        c2 = s1.copy()
                        # last_item_s2 = s2[-1][-1]
                        last_c2 = c2[-1].copy()
                        last_c2.append(s2[-1][-1])
                        # c2 = removeItem(c2,get_length(c2)-1)
                        del (c2[-1])
                        c2.append(last_c2)
                        C.append(c2)

            elif (MIS[last_s2] < getMISofSequence(s2, MIS, last_s2)):
                if ((removeItem(s2, 1) == removeItem(s1, get_length(s1) - 1)) & (MIS[first_s1] > MIS[last_s2])):
                    if (len(s1[0]) == 1):
                        c1 = []
                        c1 = s2.copy()
                        c1.append([s1[0][0]])
                        C.append(c1)

                        if ((get_length(s2) == 2 & len(s2) == 2) & (MIS[first_s1] > MIS[first_s2])):
                            c2 = []
                            c2 = s2.copy()
                            last_c2 = c2[0].copy()
                            last_c2.append(s1[0][0])
                            # c2 = removeItem(c2,0)
                            del (c2[0])
                            c2.append(last_c2)
                            C.append(c2)
                    elif (((get_length(s2) == 2 & len(s2) == 1) & (MIS[first_s1] > MIS[first_s2])) | (
                            get_length(s2) > 2)):
                        c2 = []
                        c2 = s2.copy()
                        # last_item_s1 = s1[0][0]
                        last_c2 = c2[0].copy()
                        last_c2.append(s1[0][0])
                        # c2 = removeItem(c2,0)
                        del (c2[0])
                        c2.append(last_c2)
                        C.append(c2)

            else:
                if (removeItem(s1, 0) == removeItem(s2, get_length(s2) - 1)):
                    if len(s2[-1]) == 1:
                        c1 = []
                        c1 = s1.copy()
                        c1.append([s2[-1][-1]])
                        C.append(c1)

                    else:
                        c1 = []
                        c1 = s1.copy()
                        # last_item_s2 = s2[-1][-1]
                        last_c1 = c1[-1].copy()
                        last_c1.append(s2[-1][-1])
                        # c1 = removeItem(c1,get_length(c1)-1)
                        del (c1[-1])
                        c1.append(last_c1)
                        C.append(c1)

    prune_c = PruneC(C, F, MIS)
    return prune_c


def PruneC(Can_Seq, F, M):
    count = 0;
    final_Can_Seq = []
    for Can_Seq_Item in Can_Seq:
        count = 0
        temp_Can_Seq = deepcopy(Can_Seq_Item)
        temp_list = []
        for Can_Seq_Si, Can_Seq_Item_Seq in enumerate(Can_Seq_Item):
            min_MS_Can_Seq_Item = ''
            min_MS_Can_Seq_Item = Can_Seq_Item_Seq[0]
            for e_item in Can_Seq_Item_Seq:
                if (M[e_item] < M[min_MS_Can_Seq_Item]):
                    min_MS_Can_Seq_Item = e_item
            for Can_Seq_Ii, Can_Seq_Item_item in enumerate(Can_Seq_Item_Seq):
                temp_Can_Seq = deepcopy(Can_Seq_Item)
                if (temp_Can_Seq[Can_Seq_Si][Can_Seq_Ii] != min_MS_Can_Seq_Item):
                    del temp_Can_Seq[Can_Seq_Si][Can_Seq_Ii]
                    temp_Can_Seq = list(filter(None, temp_Can_Seq))
                    temp_list.append(temp_Can_Seq)
        temp = 0
        for each_temp_list in temp_list:
            if (not any(each_temp_list == each_items for each_items in F)):
                temp += 1
        if (temp == 0):
            final_Can_Seq.append(Can_Seq_Item)
    return final_Can_Seq


def removeItem(s, index):
    seqnew = copy.deepcopy(s)
    length = get_length(s)
    if index < 0 or index >= length:
        return []
    count = 0
    for element in seqnew:
        if count + len(element) <= index:
            count += len(element)
        else:
            del element[index - count]
            break
    return [element for element in seqnew if len(element) > 0]


def getMISofSequence(s, MIS, item):
    temp = []
    MIS_array = []
    for i in s:
        for j in range(len(i)):
            temp.append(i[j])

    temp.remove(item)

    for elem in temp:
        MIS_array.append(MIS[elem])

    return min(MIS_array)


def get_length(s):
    return sum(len(i) for i in s)
