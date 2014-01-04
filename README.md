Complete-Seq RNAseq Pipeline:

Ready to test on Minerva cluster to generate and launch PBS scripts for tophat mapping jobs first (Server functionality in the works, as well as generalized PBS environment deployment)

To begin testing:
  1. Login to Minerva
  2. git clone "git@github.com:shenlab-sinai/complete-seq.git"
  3. cd /complete-seq/src/
  4. edit config_template.yaml to set paths to your respective home and genome directories. Scratch space usage is recommended.
  5. Create input file to for mapping run using pipeline_start_template.yaml as a basis for required parameters.
  6. Usage:
     - python ./src/complete_seq.py -p {config file}.yaml
