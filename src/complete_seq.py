#!/usr/bin/python
import optparse
from analysis_framework import *
from env_config import *

parser = optparse.OptionParser()
parser.add_option('-p', dest="pipeline_input")
options, remainder = parser.parse_args()

settings = ImportSettings() #enviroment configuration settings

def main():
	

	pipeline_command = UserInputsConfigFile(options.pipeline_input)
	directories  = SetProjectEnv(settings.homeDir(),pipeline_command.projName())
	writer = ScriptWriter() #simplify this
	
	directories.makeProj() #project directory created
	directories.startMappingEnv() #mapping subdirectories created
	writer.writeMappingScript(options.pipeline_input)

if __name__ == '__main__':
    main()