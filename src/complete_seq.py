#!/usr/bin/python
import optparse
from analysis_framework import *
from env_config import *
from utils import *


parser = optparse.OptionParser()
parser.add_option('-p', dest="pipeline_input")
parser.add_option('-m', dest="merge_table")
options, remainder = parser.parse_args()

settings = ImportSettings() #enviroment configuration settings
util = Utility()
def main():
	
	#mapping
	pipeline_command = UserInputsConfigFile(options.pipeline_input)
	if pipeline_command.openConfig()["mapping"] is not None:

		directories  = SetProjectEnv(settings.homeDir(),pipeline_command.projName())
		writer = ScriptWriter() #simplify this
		
		directories.makeProj() #project directory created
		directories.startMappingEnv() #mapping subdirectories created
		writer.writeMappingScript(options.pipeline_input,options.merge_table)

		#if pipeline_command.openConfig()["mapping"][ merge_directory_path] is not None:
			#mergetable outer logic
		#util.batchQsub(settings.homeDir()+"/"+pipeline_command.projName()+"/scripts/mapping/") #omit for testing purposes

if __name__ == '__main__':
    main()