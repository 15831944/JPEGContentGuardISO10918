#!/usr/bin/env python2.7


# This script executes a libjpeg 6b djpeg with guard test.


import os
import sys
import utils


# Executes a djpeg test.
# name: string name of test.
def Execute (name):

   # 1. Setup some path variables.
   configFileName = name + ".cfg"
   curDir = os.getcwd ()
   configDir = os.path.join (curDir, "configs")
   testDir = os.path.join (curDir, name)
   configFile = os.path.join (configDir, configFileName)
   acceptDir = utils.GetAcceptDir (configFile)
   djpegDir = os.path.join (testDir, "djpeg-6b-guard")
   codeDir = os.path.join (djpegDir, "jpeg-6b")

   # 2. Setup test envrionment.
   utils.Djpeg6bSetup (testDir, djpegDir)

   # 3. Execute the test.
   utils.RunDjpegTest (codeDir, acceptDir)

   # 4. Generate the analysis information.
   utils.GenerateAnalysisData (codeDir, name + "-djpg-6b-and-guard")

   # 5. Display the analysis information.
   utils.DisplayAnalysisData (codeDir)


###############################################################################
# Script Execution.
###############################################################################

if __name__ == '__main__':

   # Execute
   Execute (sys.argv[1])





