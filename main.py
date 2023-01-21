import dxfFunctionality
import optimisationUtilities


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filename = "1.dxf"
    arrayOfVectors = dxfFunctionality.dxfToVectors(filename)  # potentially, will break with points

    print(arrayOfVectors)

    sortedArray = optimisationUtilities.optimiseOrderOfVectors(arrayOfVectors)

    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
