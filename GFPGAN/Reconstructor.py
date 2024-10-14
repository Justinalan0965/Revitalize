import os

def Rebuild():
    os.system('cmd /c "cd GFPGAN & conda activate gfpgan & python inference_gfpgan.py -i inputs/whole_imgs -o results -v 1.4 -s 2"')
    os.system('cmd /c "conda deactivate"')
    