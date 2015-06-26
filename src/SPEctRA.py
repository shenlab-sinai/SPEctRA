#!/usr/bin/python
import optparse
from analysis_framework import *
from env_config import *
from utils import *


parser = optparse.OptionParser()
parser.add_option('-p', dest="pipeline_input")
parser.add_option('-m', dest="merge_table")
options, remainder = parser.parse_args()

settings = ImportSettings()  # enviroment configuration settings
util = Utility()


def main():
    # mapping

    pipeline_command = UserInputsConfigFile(options.pipeline_input)
    if pipeline_command.openConfig()["mapping"] is not None:

        directories = SetProjectEnv(
            settings.homeDir(), pipeline_command.projName())
        writer = ScriptWriter()  # simplify this

        directories.makeProj()  # project directory created
        directories.startMappingEnv()  # mapping subdirectories created
        writer.writeMappingScript(options.pipeline_input, options.merge_table)
        # omit for testing purposes
        if settings.getEnv()["cluster"] is not None:
            util.batchBsub(
                settings.homeDir() + "/" + pipeline_command.projName() + "/scripts/mapping/")
        # Server logic added 
        if settings.getEnv()["server"] is not None:
            util.chmodAll(
                settings.homeDir() + "/" + pipeline_command.projName() + "/scripts/mapping/")
            util.chmodAll(
                settings.homeDir() + "/" + pipeline_command.projName() + "/scripts/counts/")
            util.chmodAll(
                settings.homeDir() + "/" + pipeline_command.projName() + "/scripts/QC/")
            util.chmodAll(
                settings.homeDir() + "/" + pipeline_command.projName() + "/scripts/")
            os.system("/"+settings.homeDir() + "/" + pipeline_command.projName() + "/scripts/mappingMaster.sh")


if __name__ == '__main__':
    main()
