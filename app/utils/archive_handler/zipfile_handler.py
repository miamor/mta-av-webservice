import zipfile
import os


def unzipfile(filename, path_to_extract):
    if not filename:
        raise Exception("The " + filename.__str__ + " doest not exist. Please check again.")
    if not os.path.isfile(filename):
        raise Exception("File doest not exist. Please check again.")
    zip = zipfile.ZipFile(file=filename, mode='r')
    zip.extractall(path=path_to_extract)
    zip.close()


def test_unzip():
    import os
    filename = os.path.dirname(os.path.dirname(__file__))+'/data/zipfiles/Digi4-20180801.zip'
    path_to_extract = os.path.dirname(os.path.dirname(__file__))+'/data/zipfiles/csv'
    try:
        unzipfile(filename=filename, path_to_extract=path_to_extract)
    except:
        print('Could not extract zip file')

if __name__ == '__main__':
    test_unzip()