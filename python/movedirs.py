import os
import shutil


path = 'c:\\projects\\hc2\\'
path = os.path.join("content", "videos")
folders = []

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for folder in d:
        # folders.append(os.path.join(r, folder))
        folders.append(folder)
        print("folder " + folder)
        oldname = os.path.join(r, folder,"index.md")
        newname =  os.path.join(r, folder + "-.md")
        print ("move from " + oldname + " to " + newname )
        shutil.move(oldname, newname)
# for f in folders:
#     print(f)
