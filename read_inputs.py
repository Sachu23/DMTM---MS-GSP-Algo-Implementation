import re
import math


def _get_sequence(contents):
    seq_list = []
    temp = []
    temp_1 = []
    for line in contents:
        line = line.strip()[1:-1]

        for s in re.split(r'}{', line[1:-1]):
            for i in re.split(',| ', s):
                if i != '':
                    temp.append(int(i))

            temp_1.append(temp)
            temp = []
        seq_list.append(temp_1)
        temp_1 = []

    return seq_list


def read_seq_file():
    # Reading Sequence file - data.txt
    with open('input files/data2.txt', 'rt') as file:
        contents = [x.strip() for x in file.read().split("\n")]
        seq_list = _get_sequence(contents)

    return seq_list


def _get_mis_and_sdc(contents):
    min_sup = dict()
    sdc = math.inf
    for line in contents:
        if line.strip() != '':
            if "SDC" not in line:
                input = int(re.findall('MIS\((.*?)\)', line)[0])
                value = float(line.strip().split('=')[1])
                min_sup[input] = value

            else:
                sdc = float(line.strip().split("=")[1])

    return min_sup, sdc


def read_param_file():
    # Reading requirements file
    with open('input files/para2-2.txt', 'rt') as file:
        contents = [x.strip() for x in file.read().split("\n")]
        mis, sdc = _get_mis_and_sdc(contents)

    return mis, sdc
