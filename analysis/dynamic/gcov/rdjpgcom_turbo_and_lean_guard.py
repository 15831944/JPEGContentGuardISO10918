#!/usr/bin/env python2.7


# This script executes a libjpeg turbo rdjpgcom turbo with lean guard test.


import os
import sys
import utils


# Executes a djpeg test.
# name: string name of test.
def Execute (name):

   # 1. Setup some path variables.
   curDir = os.getcwd ()
   testDir = os.path.join (curDir, name)
   acceptDir = utils.GetLeanAcceptDir ()
   rdjpgcomDir = os.path.join (testDir, "rdjpgcom-turbo")
   codeDir = os.path.join (rdjpgcomDir, "libjpeg-turbo-2.0.4")

   # 2. Setup test envrionment.
   utils.DjpegTurboSetup (testDir, rdjpgcomDir)

   # 3. Execute the test.
   utils.RunRdjpgcomTest (codeDir, acceptDir)

   # 4. Generate the analysis information.
   utils.GenerateAnalysisData (codeDir, name + "-and-rdjpgcom-turbo")

   # 5. Display the analysis information.
   utils.DisplayAnalysisData (codeDir)


###############################################################################
# Script Execution.
###############################################################################

if __name__ == '__main__':

   # Execute
   Execute (sys.argv[1])





