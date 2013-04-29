#!/usr/bin/env python
import os
import sys
import re
import shutil
import urllib
import pdb

class myDirecory:
	Name = ""
	Path = ""
	lowCaseName = ""
	
class myFile:
	Name = ""
	lowCaseName = ""
	Path = ""
	def CopyTo(self, targetPath, OverWrite):
		fileNameDest = os.path.join(targetPath,self.Name)
		print "target patch " + targetPath
		if os.path.isfile(fileNameDest):
			if OverWrite:
				os.remove(fileNameDest)
			else:
				print "File already exist"
				return
		try:
			shutil.copy( self.Path , fileNameDest)
			print "copy " + self.Path + " -> " + fileNameDest 
		except:
			print "Error in File IO operation"
		return

	def MoveTo(self, targetPath, OverWrite):
		#print "target patch " + targetPath
		#print "self.Name " + self.Name
		fileNameDest = os.path.join(targetPath,self.Name)
		#print "fileNameDest " + fileNameDest
		if os.path.isfile(fileNameDest):
			if OverWrite:
				os.remove(fileNameDest)
			else:
				print "File already exist"
				return
		try:
			print "Move {0} -> {1}".format( self.Path, fileNameDest)
			shutil.move( self.Path , fileNameDest)
		except:
			print "Error in File IO operation"
		return

#
#	get list of dir
#
def listdirs(folder):
	return [d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
        if os.path.isdir(d)]
#
#	get list of file
#
def listfiles(folder):
	return [d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
        if os.path.isfile(d)]
#
#	splace not alpha caraceter
#
def strClean(str):
	c = ""
	for index in range (len(str)):
		if ( (str[index].isalnum())==False):
			c += ' '
		else:
			c += str[index]
				
	while (c.find("  ") > -1):
		c = c.replace ("  "," ")
	return c
	
def ScanInputPath(path):
	print "Scanning input patch " + path
	fileList = list()
	regex = re.compile("[sS]?\d?\d[xXeEsS]\d\d")# re 00x11 or 0x11 or 00X11 or 0X11 or S01E01 or s01s02
	#	scan file
	for fileNamePath in listfiles(path):
		#fileName = fileNamePath.replace(path,"") 	#remove base path
		fileName = os.path.basename(fileNamePath) 	#remove base path
		match = regex.findall(fileName)
		if(len(match) >0):
			t = myFile()
			t.Name = fileName
			t.Path = fileNamePath
			#remove all chare befoar s01x02
			print "Input file " + fileName
			t.lowCaseName = strClean(fileName[0:fileName.index(match[0])]).lower().strip()
			fileList.append(t)
	return fileList
	
def ScanOutPath(path):
	OutPathList = list()
	print "Scanning out path " + path
	#	Load directory and clean
	for dirName in listdirs(path):
		if (dirName.find('./.') == -1):
			t = myDirecory()						# make data container
			t.Name = dirName.replace(path," ")		# remove base path
			t.Path = dirName						# complete path
			t.lowCaseName = strClean(t.Name.lower()).strip()
			OutPathList.append(t)
	return OutPathList
	
def ShowHelp():
	print 'APCT - Anti Paranoya Copy Tool'
	print 'operand:'
	print '\t-i <Input_Path>'
	print '\t-o <Output_Path>'
	print '\t--help or -h		Help'
	print ''
	print 'example:'
	print '\tapct.py -i /home/user/download/ /home/xbmc/TvShows/'
	

#
#	Main Code
#
def main(argv): 
	outDirecotryList = list()
	inListFile = list()
	index = 0
	
	if(len(argv) == 0):
		print 'apct: Missing file operand'
		ShowHelp()
		return

	while (index < len(argv)):
		# scan parameters
		increase_step = 1
		#  input directory
		if (argv[index] == '-i'):
			if(os.path.isdir(argv[index+1]) == False):
				print "Error: " + argv[index+1] + " is not a directory"
				return 
			myDir = os.path.abspath(argv[index+1])
			inListFile += ScanInputPath(myDir)
			increase_step = 2
		# -o parametrers
		if (argv[index] == '-o'):
			if(os.path.isdir(argv[index+1]) == False):
				print "Error: " + argv[index+1] + " is not a directory"
				return
			myDir = os.path.abspath(argv[index+1])
			outDirecotryList += ScanOutPath(myDir)
			increase_step = 2
		if(argv[index] == '--help'):
			ShowHelp()
			return

		if(argv[index] == '-h'):
			ShowHelp()
			return
		
		index += increase_step 

	print "Moving or Coping ##################################"
	counter = 0
	for file in inListFile:
		targerDir = None
		for dir in outDirecotryList:
			##rc = dir.lowCaseName.find(file.lowCaseName)
			##if(rc != -1):
			if(dir.lowCaseName == file.lowCaseName):
				targerDir = dir
				
		if(targerDir != None):
			counter += 1
			file.MoveTo(targerDir.Path, True)
			
	if(counter > 0):
		myUrl = urllib.urlopen("http://localhost:8080/xbmcCmds/xbmcHttp?command=ExecBuiltIn(UpdateLibrary(Video))")
		s = myUrl.read()
		myUrl.close()

if __name__ == "__main__":
	main(sys.argv[1:])
