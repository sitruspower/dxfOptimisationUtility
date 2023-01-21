import ezdxf
import sys
import numpy as np


# helper function
def printEntity(entity):
    print("LINE on layer: %s" % entity.dxf.layer)
    print("start point: %s" % entity.dxf.start)
    print("end point: %s\n" % entity.dxf.end)


def readDxf(filename):
    # print("reading the DFX from file: ", filename)
    try:
        doc = ezdxf.readfile(filename)
        return doc
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        sys.exit(2)


def dxfToVectors(filename):
    '''
    convert given DXF into array of vectors in the following manner:
     | Xs  | Ys | Xf  | Yf |
     | 1.  | 2. | 3.  | 4. |
    Z is neglected (all is 0).
    :param filename:  name of the dxf file
    :return: Nx4 array  with array[n, 0] = Xstart array[n, 1]=Xfinish, array[n, 2]=Ystart array[n, 3]= Yfinish
    '''

    doc = readDxf(filename)
    msp = doc.modelspace()  # return modelspace by default
    numberOfItemsTotal = len(msp)  # total number of items

    group = ezdxf.groupby.groupby(entities=msp, dxfattrib="layer")  # group dxf by layers
    numberOfILayers = len(group)

    vectorArray = np.empty([4,numberOfItemsTotal])

    itemCount = 0
    # only single layer operation is used for now. Expand to multilayer in future.
    for layer, entities in group.items():
        print(f'Layer "{layer}" contains following entities:')
        for entity in entities:
            vectorArray[itemCount, 0] = entity.dxf.start[0]
            vectorArray[itemCount, 1] = entity.dxf.start[1]
            vectorArray[itemCount, 2] = entity.dxf.end[0]
            vectorArray[itemCount, 3] = entity.dxf.end[1]
            itemCount += 1

    # print(vectorArray)
    return vectorArray




