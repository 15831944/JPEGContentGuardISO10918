#!/usr/bin/env python2.7


# Utility methods for gcov analysis scripts.


import os
import subprocess
import patch
import time


# Gets the directory for the sample images.
def GetSampleDir ():
   curDir = os.getcwd ()
   os.chdir ("../../../samples")
   sampleDir = os.getcwd ()
   os.chdir (curDir)
   return (sampleDir)


# Gets the diretory for the djpeg source code.
def GetDjpegSrcDir ():
   curDir = os.getcwd ()
   os.chdir ("../../../jpeg-6b")
   djpegSrcDir = os.getcwd ()
   os.chdir (curDir)
   return (djpegSrcDir)


# Gets the diretory for the guard source code.
def GetGuardSrcDir ():
   curDir = os.getcwd ()
   os.chdir ("../../../guard")
   guardSrcDir = os.getcwd ()
   os.chdir (curDir)
   return (guardSrcDir)


# Gets the diretory for the patches code.
def GetPatchDir ():
   curDir = os.getcwd ()
   patchDir = os.path.join (curDir, "patches")
   return (patchDir)


# Copy the libjpeg files over.
# copyDir: Where to copy the files over.
def CopyLibJpegFiles (copyDir):
   djpegSrcDir = GetDjpegSrcDir ()
   cmd = ["cp", "-r", djpegSrcDir, copyDir]
   subprocess.call (cmd)


# Copy the guard files over.
# copyDir: Where to copy the files over.
def CopyGuardFiles (copyDir):
   guardSrcDir = GetGuardSrcDir ()
   cmd = ["cp", "-r", guardSrcDir, copyDir]
   subprocess.call (cmd)


# Applies the necesary gcov patches.
# patchDir: Where the patch files are located.
# codeDir: Where the apply the patches.
# patchFile: patch file to apply.
def Patch (patchDir, codeDir, patchFile):
   patch1 = os.path.join (patchDir, patchFile)
   curDir = os.getcwd ()
   os.chdir (codeDir)
   pset = patch.fromfile (patch1)
   pset.apply ()
   os.chdir (curDir)


# Configures source code for compilation.
# codeDir:  Where the source code is located.
def Configure (codeDir):
   curDir = os.getcwd ()
   os.chdir (codeDir)
   cmd = ["./configure"]
   subprocess.call (cmd)
   os.chdir (curDir)


# Executes the cmake command to setup the make system.
# codeDir:  Where the source code is located.
def Cmake (codeDir):
   curDir= os.getcwd ()
   os.chdir (codeDir)
   cmd = ["cmake", codeDir]
   subprocess.call (cmd)
   os.chdir (curDir)


# Builds the source code.
# codeDir:  Where the source code is located.
def Build (codeDir):
   curDir = os.getcwd ()
   os.chdir (codeDir)
   cmd = ["make"]
   subprocess.call (cmd)
   os.chdir (curDir)


# Sets up the test environment for a djpeg test.
# testDir: Where to setup the test.
# djpegDir: Where to setup the djpeg stuff for the test.
def DjpegSetup (testDir, djpegDir):

   print "---> Setting up test envrionment ..."
   print "   --- Making directories ... "
   os.mkdir (djpegDir)
   print "   --- Copying libjpeg source files ... "
   CopyLibJpegFiles (djpegDir)
   print "   --- Patching libjpeg config file."
   patchDir = GetPatchDir ()
   codeDir = os.path.join (djpegDir, "jpeg-6b")
   Patch (patchDir, codeDir, "djpeg.patch.1")
   print "   --- Executing the configure setup script."
   Configure (codeDir)
   print "   --- Patching libjpeg Make file."
   Patch (patchDir, codeDir, "djpeg.patch.2")
   print "   --- Making the libjpeg code."
   Build (codeDir)
   print "---> Finished setting up test envrionment."


# Sets up the test environment for a rdjpgcom test.
# testDir: Where to setup the test.
# rdjpgcomDir: Where to setup the rdjpgcom stuff for the test.
def RdjpgcomSetup (testDir, rdjpgcomDir):

   print "---> Setting up test envrionment ..."
   print "   --- Making directories ... "
   os.mkdir (rdjpgcomDir)
   print "   --- Copying libjpeg source files ... "
   CopyLibJpegFiles (rdjpgcomDir)
   print "   --- Patching libjpeg config file."
   patchDir = GetPatchDir ()
   codeDir = os.path.join (rdjpgcomDir, "jpeg-6b")
   Patch (patchDir, codeDir, "djpeg.patch.1")
   print "   --- Executing the configure setup script."
   Configure (codeDir)
   print "   --- Patching libjpeg Make file."
   Patch (patchDir, codeDir, "djpeg.patch.2")
   print "   --- Making the libjpeg code."
   Build (codeDir)
   print "---> Finished setting up test envrionment."


# Sets up the test environment for a guard test.
# testDir: Where to setup the test.
# guardDir: Where to setup the guard stuff for the test.
def GuardSetup (testDir, guardDir):

   print "---> Setting up test envrionment ..."
   print "   --- Copying lig source files ... "
   CopyGuardFiles (guardDir)
   print "   --- Patching CMakeList.txt file."
   patchDir = GetPatchDir ()
   codeDir = guardDir
   Patch (patchDir, codeDir, "guard.patch.1")
   print "   --- Executing the cmake setup script."
   cmd = ["rm", "-rf", guardDir + "/CMakeCache.txt"]
   subprocess.call (cmd) 
   Cmake (codeDir)
   print "   --- Making the guard code."
   Build (codeDir)
   acceptDir = os.path.join (guardDir, "accept")
   os.mkdir (acceptDir)
   dropDir = os.path.join (guardDir, "drop")
   os.mkdir (dropDir)
   print "---> Finished setting up test envrionment."


# Runs a djpeg test.
# codeDir: Where the code is located.
# imageDir: Where the test images are located.
def RunDjpegTest (codeDir, imageDir):

   print "---> Executing the djpeg test for " + codeDir + "."
   curDir = os.getcwd ()
   os.chdir (codeDir)
   imageDir = imageDir.strip ()
   files = os.listdir (imageDir)
   for image in files:
      fullImagePath = os.path.join (imageDir, image)
      cmd = ["./djpeg", "-colors", "64", "-gif", "-scale", "1/1", "-outfile", "/dev/null", fullImagePath]
      subprocess.call (cmd)
      cmd = ["./djpeg", "-colors", "64", "-bmp", "-scale", "1/1", "-outfile", "/dev/null", fullImagePath]
      subprocess.call (cmd)
      cmd = ["./djpeg", "-colors", "64", "-os2", "-scale", "1/1", "-outfile", "/dev/null", fullImagePath]
      subprocess.call (cmd)
      cmd = ["./djpeg", "-colors", "64", "-pnm", "-scale", "1/1", "-outfile", "/dev/null", fullImagePath]
      subprocess.call (cmd)
      cmd = ["./djpeg", "-colors", "64", "-targa", "-scale", "1/1", "-outfile", "/dev/null", fullImagePath]
      subprocess.call (cmd)
   os.chdir (curDir)
   print "---> Finished djpeg test execution for " + codeDir + "."


# Runs a rdjpgcom test.
# codeDir: Where the code is located.
# imageDir: Where the test images are located.
def RunRdjpgcomTest (codeDir, imageDir):

   print "---> Executing the rdjpgcom test for " + codeDir + "."
   curDir = os.getcwd ()
   os.chdir (codeDir)
   imageDir = imageDir.strip ()
   files = os.listdir (imageDir)
   for image in files:
      fullImagePath = os.path.join (imageDir, image)
      cmd = ["./rdjpgcom", "-verbose", fullImagePath]
      subprocess.call (cmd)
   os.chdir (curDir)
   print "---> Finished rdjpgcom test execution for " + codeDir + "."


# Runs a guard test.
# exe: The location of the guard executable.
# cfgFile: Guard configuration file.
def RunGuardTest (exe, cfgFile):

   print "---> Executing the guard test for " + exe + "."
   curDir = os.getcwd ()
   cmd = [exe, "--cfg", cfgFile]
   subprocess.call (cmd)
   print "---> Finished guard test execution for " + exe + "."


# Generates the analysis information associated with a test run.
# codeDir:  Where the executed code is located.
# title:  Title name to use for the final analysis info.
def GenerateAnalysisData (codeDir, title):
   print "---> Generating analysis information ..."
   curDir = os.getcwd ()
   os.chdir (codeDir)

   # Generate the gcov statistics.
   for file in os.listdir ("."):
      if (file.endswith (".c")):
         cmd = ["gcov", "-a", "-b", file]
         subprocess.call (cmd)
      if (file.endswith (".cpp")):
         cmd = ["gcov", "-a", "-b", file]
         subprocess.call (cmd)

   # Generate the lcov analysis information.
   cmd = ["lcov", "--capture", "--directory", ".", "--output-file", "lcov.info"]
   subprocess.call (cmd)

   # Generate the html view of the analysis information.
   analysisDir = os.path.join (codeDir, "gcov_analysis")
   cmd = ["genhtml", "lcov.info", "--output-directory", analysisDir, "-t", title]
   subprocess.call (cmd)

   os.chdir (curDir)
   print "---> Finished generating analysis information."


# Displays the generated analysis information associated with a test run.
# codeDir:  Where the executed code is located.
def DisplayAnalysisData (codeDir):
   print "---> Displaying analysis information ..."
   curDir = os.getcwd ()
   analysisDir = os.path.join (codeDir, "gcov_analysis")
   os.chdir (analysisDir)
   time.sleep (1)
   os.system ("firefox -new-tab index.html &")
   os.chdir (curDir)
   print "---> Finished displaying analysis information."


# Gets the acceptance directory from a guard configuration file.
# configFile:  Guard config file.
def GetAcceptDir (configFile):

   result = "unset"
   f = open (configFile, "r")
   for line in f: 
      print line
      line = line.replace (" ", "")
      line = line.replace ("", "")
      line = line.replace ("\t", "")
      words = line.split ("=")   
      if ((len (words) == 2) and (words[0] == "accept-dir")): 
            result = words[1]
            break
   f.close ()
   print result
   return (result)



