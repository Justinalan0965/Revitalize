

# # global str1 
# str1 = "new"
# def locateFile(filename):
#     global str1
#     name = f'folder\\files\\{filename}'
#     print(name)

#     str1 = "old"


# def test():
#     print(str1)

# filename = "Kohinoor"
# locateFile(filename)
# test()
# print(str1)

# import os
# os.system('cmd /c "cd GFPGAN & conda activate gfpgan & python inference_gfpgan.py -i inputs/whole_imgs -o results -v 1.3 -s 2"')


reconstruct = True

loc1 = 'GFPGAN\inputs\whole_imgs'
loc2 = 'DeOldify\\test_images'



def printer():
    global upload
    print(upload)

def rconst():
    global reconstruct
    reconstruct = True

def color():
    global reconstruct
    reconstruct = False

# print(reconstruct)
color()
print(reconstruct)

upload = loc1 if reconstruct else loc2
rconst()
print(reconstruct)
print(upload)