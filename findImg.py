import os

dir1 = os.listdir()
for dirname in dir1:
    if os.path.isdir(dirname):
        files = os.listdir(dirname)
        for f in files:
            if f.endswith(".png"):
                print("![{0}](https://raw.githubusercontent.com/linnil1/2018_BIME_Practice/master/{1}/{0})".format(
                    f, dirname))


