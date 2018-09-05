import os, shutil

if os.path.exists('dist'):
	shutil.rmtree("dist")
if os.path.exists('build'):
	shutil.rmtree("build")
if os.path.exists('__pycache__'):
	shutil.rmtree("__pycache__")

os.system("pyinstaller -F -i images/bitbug_favicon2.ico merge-bin-as-one.py")
shutil.copyfile("dist/merge-bin-as-one.exe", "./merge-bin-as-one.exe")
shutil.rmtree("dist")
shutil.rmtree("build")
shutil.rmtree("__pycache__")
