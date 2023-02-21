import re


def read_input():
    # Reading Sequence file
    S = []
    Slines = []
    temp = []
    temp_1 = []
    with open('data.txt', 'rt') as Sfile:
        for line in Sfile:
            Slines.append(line.rstrip('\n'))
        for line in Slines:
            line = line.strip()[1:-1]

            for s in re.split(r'}{', line[1:-1]):
                for i in re.split(',| ', s):
                    if i != '':
                        temp.append(int(i))

                temp_1.append(temp)
                temp = []
            S.append(temp_1)
            temp_1 = []

    # Reading requirements file
    MIS = {}
    file = open('para.txt', 'r')
    text = file.read().split('\n')
    for line in text:
        if line.find("SDC") == -1:
            if (len(line.strip()) != 0):
                index = int(BetweenBracket(line, '(', ')').strip())
                value = float(AfterEqualTo(line, '=').strip())
                MIS[index] = value
        elif (len(line.strip()) != 0):
            SDC = float(AfterEqualTo(line, '=').strip())
    # print("S:\n", S)
    # print("MIS\n", MIS)
    # print("SDC\n", SDC)
    return S, MIS, SDC


def BetweenBracket(text, a, b):
    pos_a = text.find(a)
    if pos_a == -1:
        return ""
    pos_b = text.rfind(b)
    if pos_b == -1:
        return ""
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b:
        return ""
    return text[adjusted_pos_a:pos_b]


def AfterEqualTo(text, a):
    pos_a = text.rfind(a)
    if pos_a == -1: return ""
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(text):
        return ""
    return text[adjusted_pos_a:]
