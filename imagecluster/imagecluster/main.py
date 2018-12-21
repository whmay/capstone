import os, re
import numpy as np
import imagecluster as ic
import common as co


# from imagecluster import imagecluster as ic
# from imagecluster import common as co
pj = os.path.join


ic_base_dir = 'imagecluster'

def printDict(dictionary):
    for key, value in dictionary.items():
        print(key, value)

def help(imagedir,clusters):
    dict = {}
    names = []
    for imList in clusters:
        if len(imList) not in dict:
            dict[len(imList)] = 1
        else:
            dict[len(imList)] = dict[len(imList)] + 1
        index1 = dict[len(imList)]
        index2 = 1
        for im in imList:
            oldname = im
            updatedName =imagedir +"/"+ str(len(imList)) +"_"+ str(index1) +"_"+ str(index2) +".jpg"
            index2 = index2 + 1
            os.rename(oldname, updatedName)
            names.append(updatedName)
    # names.sort()
    # for name in names:
    #     print(name)
    # printDict(dict)

def main(imagedir, sim=0.5):
    """Example main app using this library.

    Parameters
    ----------
    imagedir : str
        path to directory with images
    sim : float (0..1)
        similarity index (see imagecluster.cluster())
    """
    dbfn = pj(imagedir, ic_base_dir, 'fingerprints.pk')
    # print("dbfn= " + dbfn)
    if not os.path.exists(dbfn):
        os.makedirs(os.path.dirname(dbfn), exist_ok=True)
        print("no fingerprints database {} found".format(dbfn))
        files = co.get_files(imagedir)
        model = ic.get_model()
        print("running all images through NN model ...".format(dbfn))
        fps = ic.fingerprints(files, model, size=(224,224))
        # print(fps)
        co.write_pk(fps, dbfn)
    else:
        print("loading fingerprints database {} ...".format(dbfn))
        fps = co.read_pk(dbfn)
    print("clustering ...")
    print(len(fps))

    clusters =ic.cluster(fps, sim)
    help(imagedir,clusters)

    ic.make_links(ic.cluster(fps, sim), pj(imagedir, ic_base_dir, 'clusters'))


if __name__ == "__main__":

    with open("../data/sights.txt") as f:
        lines = [line.rstrip('\n') for line in f]
    for line in lines:
        fp = os.path.join("/Users/hao/Desktop/imagecluster/data/dataset/", line)
        main(fp, 0.48)

