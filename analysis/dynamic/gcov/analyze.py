#!/usr/bin/env python2.7


# This script performs gcov dynamic analysis analysis on the djpeg and rdjpgcom 
# executables in libjpeg.


import subprocess
import patch
import os
import time


# Cleans the eviornment (directory) for a fresh run.
def Clean ():
   print "---> Cleaning directory ..."
   cmd = ["rm", "-rf", "djpeg", "rdjpgcom", "djpeg_analysis", "rdjpgcom_analysis"]
   subprocess.call (cmd)
   print "---> Cleaned."


# Copy the libjpeg files over.
def CopyLibJpegFiles ():
   print "---> Copying libjpeg fies over ..."
   cmd = ["cp", "-r", "../../../jpeg-6b", "."]
   subprocess.call (cmd)
   cmd = ["mv", "jpeg-6b", "djpeg"]
   subprocess.call (cmd)
   cmd = ["cp", "-r", "../../../jpeg-6b", "."]
   subprocess.call (cmd)
   cmd = ["mv", "jpeg-6b", "rdjpgcom"]
   subprocess.call (cmd)
   print "---> Copied libjpeg files."


# Applies the configure patches to remove optimization and add gcov flags.
def PatchConfigFiles ():
   print "---> Patching confgure files with gcov settings ..."
   pset = patch.fromfile ("djpeg.patch.1")
   pset.apply ()
   pset = patch.fromfile ("rdjpgcom.patch.1")
   pset.apply ()
   print "---> Patched configure files."


# Applies the makefile patches to link in the gcov code.
def PatchMakeFiles ():
   print "---> Patching Makefiles with gcov settings ..."
   pset = patch.fromfile ("djpeg.patch.2")
   pset.apply ()
   pset = patch.fromfile ("rdjpgcom.patch.2")
   pset.apply ()
   print "---> Patched Makefiles."


# Executes a command in the provided sub directory.
# @param[in] sub_dir String of the subdirectory name.
# @param[in] cmd String of the command to execute.
def ExecuteSubDirCommand (sub_dir, cmd):
   print "---> Executing " + cmd + " for " + sub_dir 
   
   # Get the script execution directory.
   script_dir = os.getcwd () 

   # Switch directories.
   new_dir = os.path.join (script_dir, sub_dir) 
   os.chdir (new_dir)

   # Execute the command.
   new_cmd = [cmd]
   subprocess.call (new_cmd)

   # Change back to the script directory.
   os.chdir (script_dir)

   print "---> Executed " + cmd + " for " + sub_dir 


# Executes the configure command to setup the make system.
def ExecuteConfigure ():
   ExecuteSubDirCommand ("djpeg", "./configure")  
   ExecuteSubDirCommand ("rdjpgcom", "./configure")  


# Builds the binary executables.
def BuildExecutables ():
   ExecuteSubDirCommand ("djpeg", "make")  
   ExecuteSubDirCommand ("rdjpgcom", "make")  


# Runs the djpeg test.
def RunDjpegTest ():
   print "---> Executing the djpeg test ..."

   # Get the script execution directory.
   script_dir = os.getcwd () 

   # Switch directories.
   djpeg_dir = os.path.join (script_dir, "djpeg") 
   os.chdir (djpeg_dir)

   # Build the execution command.
   cmd = ["./djpeg", "-colors", "64", "-gif", "-scale", "1/1", "-outfile", "junk.gif", "testprog.jpg"]
   subprocess.call (cmd)
   
   # Change back to the script directory.
   os.chdir (script_dir)

   print "---> Finished executing the djpeg test."


# Runs the djpeg test.
def RunRdjpegcomTest ():
   print "---> Executing the rdjpgcom test ..."

   # Get the script execution directory.
   script_dir = os.getcwd () 

   # Switch directories.
   rdjpgcom_dir = os.path.join (script_dir, "rdjpgcom") 
   os.chdir (rdjpgcom_dir)

   # Build the execution command.
   cmd = ["./rdjpgcom", "-verbose", "testorig.jpg"]
   subprocess.call (cmd)
   
   # Change back to the script directory.
   os.chdir (script_dir)

   print "---> Finished executing the rdjpgcom."


# Generates analysis information for a subdirectory for a given run.
# @param[in] sub_dir String of the subdirectory to create analysis data for.
def GenerateSubDirAnalysis (sub_dir):
   print "---> Generating the analysis data for " + sub_dir + "."

   # Get the script execution directory.
   script_dir = os.getcwd () 

   # Switch directories.
   new_dir = os.path.join (script_dir, sub_dir) 
   os.chdir (new_dir)

   # Generate the gcov statistics.
   for file in os.listdir ("."):
      if (file.endswith (".c")):
         cmd = ["gcov", "-a", "-b", file]
         subprocess.call (cmd)

   # Generate the lcov analysis information.
   cmd = ["lcov", "--capture", "--directory", ".", "--output-file", "lcov.info"]
   subprocess.call (cmd)

   # Generate the html view of the analysis information.
   analysis_dir = os.path.join (script_dir, sub_dir + "_analysis")
   cmd = ["genhtml", "lcov.info", "--output-directory", analysis_dir]
   subprocess.call (cmd)

   # Change back to the script directory.
   os.chdir (script_dir)

   print "---> Finished generating analysis data for " + sub_dir + "."


# Generates analysis information for a run.
def GenerateAnalysis ():
   GenerateSubDirAnalysis ("djpeg")
   GenerateSubDirAnalysis ("rdjpgcom")


# Executes a step of sequences to produce the output data.
def Execute ():

   # 1. Clean out an remnants of previous runs.
   Clean ()

   # 2. Copy over a fresh copy of the libjpeg source code. 
   CopyLibJpegFiles ()

   # 3. Patch the configure files.
   PatchConfigFiles ()

   # 4. Execute the configure command.
   ExecuteConfigure ()

   # 5. Patch the makefiles.
   PatchMakeFiles ()

   # 6. Build the executables.
   BuildExecutables ()

   # 7. Run the tests on each executable.
   RunDjpegTest ()
   RunRdjpegcomTest ()

   # 8. Generate the analysis information.
   GenerateAnalysis ()

   # 9. Display the analysis information.
   os.system ("firefox -new-tab djpeg_analysis/index.html &")
   time.sleep (1)
   os.system ("firefox -new-tab rdjpgcom_analysis/index.html &")


###############################################################################
# Script Execution.
###############################################################################

if __name__ == '__main__':

   # Execute.
   Execute ()





