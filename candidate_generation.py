import copy
from copy import deepcopy


def level_2(L, MIS, n, sdc):
    C2 = []
    for i in range(0, len(L)):
        C2.append([[L[i][0]], [L[i][0]]])
        C2.append([[L[i][0], L[i][0]]])
        if (L[i][1] / n) >= MIS[L[i][0]]:
            for j in range(i + 1, len(L)):
                if ((L[j][1] / n) >= MIS[L[i][0]]) & (abs(L[j][1] / n - L[i][1] / n) <= sdc):
                    if L[i][0] < L[j][0]:
                        C2.append([[L[i][0], L[j][0]]])
                    else:
                        C2.append([[L[j][0], L[i][0]]])
                    C2.append([[L[i][0]], [L[j][0]]])
                    C2.append([[L[j][0]], [L[i][0]]])
    return C2


def ms_gsp_candidate_gen(F, M, CountMap, SDC, MIS):
    # F[2] = [[[20, 30]], [[20], [30]], [[20, 70]], [[20], [70]], [[20], [80]], [[30], [30]], [[30, 70]], [[30], [70]], [[30, 80]], [[30], [80]], [[70], [70]], [[70, 80]], [[80], [70]], [[10, 40]], [[10], [40]], [[40], [40]]]
    # F[2] = [[[20, 30, 40]], [[40], [70]]]
    # print(F)
    C = []
    for i in F:
        for j in F:
            s1 = i
            s2 = j
            first_s1 = getFirstItem(s1)
            last_s1 = getLastItem(s1)
            first_s2 = getFirstItem(s2)
            last_s2 = getLastItem(s2)
            MIS_least_seq = getMISofSequence(s1, MIS, first_s1)
            # print(s1)
            # print(s2)

            if (MIS[first_s1] < MIS_least_seq):
                if ((removeItem(s1, 1) == removeItem(s2, Length(s2) - 1)) & (MIS[last_s2] > MIS[first_s1])):
                    if (Size(LastElement(s2)) == 1):
                        c1 = []
                        c1 = s1.copy()
                        c1.append([getLastItem(s2)])
                        C.append(c1)

                        if ((Length(s1) == 2 & Size(s1) == 2) & (MIS[last_s2] > MIS[last_s1])):
                            c2 = []
                            c2 = s1.copy()
                            last_c2 = LastElement(c2).copy()
                            last_c2.append(getLastItem(s2))
                            # c2 = removeItem(c2,Length(c2)-1)
                            del (c2[-1])
                            c2.append(last_c2)
                            C.append(c2)

                    elif (((Length(s1) == 2 & Size(s1) == 1) & (MIS[last_s2] > MIS[last_s1])) | (Length(s1) > 2)):
                        c2 = []
                        c2 = s1.copy()
                        # last_item_s2 = getLastItem(s2)
                        last_c2 = LastElement(c2).copy()
                        last_c2.append(getLastItem(s2))
                        # c2 = removeItem(c2,Length(c2)-1)
                        del (c2[-1])
                        c2.append(last_c2)
                        C.append(c2)

            elif (MIS[last_s2] < getMISofSequence(s2, MIS, last_s2)):
                if ((removeItem(s2, 1) == removeItem(s1, Length(s1) - 1)) & (MIS[first_s1] > MIS[last_s2])):
                    if (Size(FirstElement(s1)) == 1):
                        c1 = []
                        c1 = s2.copy()
                        c1.append([getFirstItem(s1)])
                        C.append(c1)

                        if ((Length(s2) == 2 & Size(s2) == 2) & (MIS[first_s1] > MIS[first_s2])):
                            c2 = []
                            c2 = s2.copy()
                            last_c2 = FirstElement(c2).copy()
                            last_c2.append(getFirstItem(s1))
                            # c2 = removeItem(c2,0)
                            del (c2[0])
                            c2.append(last_c2)
                            C.append(c2)
                    elif (((Length(s2) == 2 & Size(s2) == 1) & (MIS[first_s1] > MIS[first_s2])) | (Length(s2) > 2)):
                        c2 = []
                        c2 = s2.copy()
                        # last_item_s1 = getFirstItem(s1)
                        last_c2 = FirstElement(c2).copy()
                        last_c2.append(getFirstItem(s1))
                        # c2 = removeItem(c2,0)
                        del (c2[0])
                        c2.append(last_c2)
                        C.append(c2)

            else:
                if (removeItem(s1, 0) == removeItem(s2, Length(s2) - 1)):
                    if (Size(LastElement(s2)) == 1):
                        c1 = []
                        c1 = s1.copy()
                        c1.append([getLastItem(s2)])
                        C.append(c1)

                    else:
                        c1 = []
                        c1 = s1.copy()
                        # last_item_s2 = getLastItem(s2)
                        last_c1 = LastElement(c1).copy()
                        last_c1.append(getLastItem(s2))
                        # c1 = removeItem(c1,Length(c1)-1)
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


def getFirstItem(s):
    first = 0
    for i in s:
        first = i[0]
        break
    return first


def getLastItem(s):
    last = 0
    for i in s:
        last = i[-1]
    return last


def removeItem(s, index):
    seqnew = copy.deepcopy(s)
    length = Length(s)
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


def Size(s):
    return len(s)


def Length(s):
    l = 0
    for i in s:
        l += len(i)
    return l


def LastElement(s):
    last = s[-1]
    return last


def FirstElement(s):
    first = s[0]
    return first
