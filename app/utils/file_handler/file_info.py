import os


def file_info_gathering(filename):
    if not filename:
        raise Exception("The file name can not be empty")
    if not os.path.isfile(filename):
        raise Exception("The file" + filename + "does not exist or corrupt. Please check again.")
    info = os.stat(filename)
    return info

def get_file_name_extension(filename):
    # if not os.path.isfile(filename):
    #     raise Exception("Can not find the file. Check again please")
    splits = os.path.splitext(filename)
    name, ext = splits[0], splits[1]
    return name, ext



# filename = os.path.dirname(os.path.dirname(__file__))+"/data/zipfiles/Digi4-20180801.zip"
# infor = file_info_gathering(filename=filename)
# print(infor.st_mtime)

# name, ext = get_file_name_extension('D:\\file.txt')
# print(name, ext)