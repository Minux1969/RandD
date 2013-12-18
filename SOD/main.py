import sys
import codecs
import csv
import time
import numpy as np
import math
import random

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

from optparse import OptionParser

def normalize_data(data):
    
    data = np.asarray(data, np.float)
    X_means = np.sum(data, 0) / data.shape[0]
    
    dataT = data.T
    ndata =[]
    count = 0
    for d in dataT:
        s = 0;
        for e in d:
            s += pow(e-X_means[count], 2)
        s = math.sqrt(s / data.shape[0])
        buff = []
        for e in d:
            buff.append((e-X_means[count]) / s)
        ndata.append(buff)
        count += 1
    ndata = np.asarray(ndata, np.float).T
    return ndata


def sampling(max, num):
    samples = []
    while(len(samples) < num):
        tmp = random.randint(0, max)
        if not tmp in samples:
            samples.append(tmp)     
    return samples

def qsp(data, sample_count):
    samples = sampling(data.shape[0] - 1, sample_count)
    i = 0
    score = []
    for d in data:
        res = 0
        for sample in samples:
            if i == sample:
                continue
            sum = 0
            for j in range(0, data.shape[1]):
                sum += pow(d[j] - data[sample][j], 2)
            if res == 0:
                res = sum
            elif sum < res:
                res = sum
        score.append(math.sqrt(res))
        i += 1
    return score, samples

def read_csv(f_path):
    try:
        f = codecs.open(f_path, "rU")
    except:
        print "Open " +  options.inuput_file + " failed!!"
        exit()
    
    is_first = True
    demention = 0
    data = []
    cnt = 1
    for row in csv.reader(f,dialect='excel'):
        if is_first:
            is_first = False
            demention = len(row)
            if demention < 1:
                return
        if len(row) != demention:
            print "Illegal data at" + str(cnt)
            return
        buff = []
        for e in row:
            buff.append(float(e))
        data.append(buff)
        cnt += 1
    return data


if __name__ == '__main__':
    parser = OptionParser()
        
    parser.add_option("-i", action = "store", dest = "input_file", type = "string", help = "Input .csv file.")
    parser.add_option("-s", action = "store", dest = "sample_count", type = "int", help = "Sample count", default = 20)
    
    (options, args) = parser.parse_args()
    if options.sample_count < 1:
        print "Sample count should be greater than 1."
        exit()
    in_data = read_csv(options.input_file)

    if in_data == None:
        exit()

    if len(in_data) <= options.sample_count:
        print "Input data count is too few, it should be greater than sample count."
        exit()

    print "Dimension : " +  str(len(in_data[0]))
    print "Data count : " + str(len(in_data))
    data = normalize_data(in_data)
    score, samples = qsp(data, options.sample_count)
    fig = pyplot.figure()
    ax = Axes3D(fig)

    inl = []
    outl = []
    cnt = 0
    sampled = []
    for s in score:
        if cnt in samples:
            sampled.append([in_data[cnt][0],in_data[cnt][1] ,s])
        elif s > 1:
            outl.append([in_data[cnt][0],in_data[cnt][1] ,s])
        else:
            inl.append([in_data[cnt][0],in_data[cnt][1] ,s])
        cnt += 1
    sampled =  np.asarray(sampled,np.float).T
    outl = np.asarray(outl,np.float).T
    inl = np.asarray(inl,np.float).T
    if len(sampled) > 0:
        ax.plot(sampled[0], sampled[1], sampled[2],"o", color="green", ms=10, mew=0.5)
    if len(outl) > 0:
        ax.plot(outl[0], outl[1], outl[2],"o", color="red", ms=4, mew=0.5)
    if len(inl) > 0:
        ax.plot(inl[0], inl[1], inl[2],"o", color="blue", ms=4, mew=0.5)
    pyplot.show()
