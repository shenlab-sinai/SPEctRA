SPEctRA RNAseq Pipeline:
=============================

###Dependencies:###
 - Python version 2.7 
 - PyYAML
 - Pysam

Ready to test on Minerva cluster to generate and launch PBS scripts for tophat mapping jobs first (Server functionality in the works, as well as generalized PBS environment deployment)

###To begin testing:###
  1. Login to Minerva
  2. git clone "git@github.com:shenlab-sinai/complete-seq.git"
  3. cd /complete-seq/src/
  4. edit config_template.yaml to set paths to your respective home and genome directories. Scratch space usage is recommended.
  5. Create input file to for mapping run using pipeline_start_template.yaml as a basis for required parameters.
     
######Pipeline Setup: [Please refer to this example configuration YAML file:](/src/config_template.yaml)
          
- The `Environment` header corresponds to the linux shell environment where you are submitting pipeline-generated jobs. This could either be a  `cluster` such as Minerva or a `server` like ngseq/gwas/medinfo
- The `project_directory` header specifies the absolute path to a directory where you wish to save <i>all</i> your pipeline-run tasks. Each task will be separated in subdirectories outlined in the [Job execution file](pipeline_start_template.yaml)
           
- The following `Short-read_aligners` are supported: `tophat` and `STAR`. Each of the corresponding subheadings must be specified with the respective module name or path. Example: 
 - `tophat2: tophat/2.0.9`
 - `bowtie2: bowtie2/2.1.0` Bowtie module <i>must</i> be specified with Tophat
 - `STAR: rna-star/2.3.0e`
 - the `genomes` header outlines paths for genomic reference and annotation files for mapping and QC. As long as the following subheader hiercarchy is adhered, the pipeline can support any built genome for tophat and STAR short-read aligners. The key subheading is the organism name. For example, for a `mouse` genome, the following YAML structure is as follows:
   


           mouse:
             rRNApath: /scratch/purusi01/Mus_musculus/Ensembl/NCBIM37/Annotation/Genes/rRNA.bed
             tophat2:
              gtf: /scratch/purusi01/Mus_musculus/Ensembl/NCBIM37/Annotation/Genes/genes.gtf
              index: /scratch/purusi01/Mus_musculus/Ensembl/NCBIM37/Sequence/Bowtie2Index/genome
             exonicPath:
             intronicPath:
             intragenicPath:
             intergenicPath:
             STAR:
               path: /scratch/purusi01/mm9_star
      
 - Please provide absolute paths to rRNA bed file, gtf and genome index files (for tophat) and STAR genome to `rRNApath`,`gtf`,`index`(under `tophat2` subheading) and `STAR``path` respectively
 (note: Mapping rates to exonic, intronic, intragenic, and intergenic features are not yet supported) 

######Pipeline Execution [Please refer to Job execution YAML file](pipeline_start_template.yaml)
- `project_Name` serves as an identification for the specific analysis (for example: RNAseq_mouse_case_vs_control) and will point to a created directory within the `project_directory` path set in the [configuration YAML file:](/src/config_template.yaml)
- `mapping` sets up the pipeline for genome alignment. Please provide the following data in the subheadings only:
 - `fastQ_directory_path` is simply the directory where your fastq files are stored. Note: data provided by the sequencing core follows a strict protocol. It is as follows:  
   - Project_Name > Sample_Name > Sample_Name_R1.fq, Sample_Name_R2.fq 
 - `proc` is the number of processors required (integer)
 - `aligner` refers to the desired short-read aligner to be used. Maps back to `tophat` and `STAR` in the [configuration YAML file:](/src/config_template.yaml)
 - `genome` refers back to the organism name in the config file, and specifically to the built genome corresponding to the short-read aligner chosen.
 - `strand`: (leave blank for now. Paired-end support is currently being tested. Leaving `strand` blank will default to "fr-unstranded" in tophat for single-end reads.
- An example pipeline execution file is as follows:


                project_Name: minerva_test
                     mapping:
                      fastQ_directory_path: /scratch/purusi01/test_fastq_pipeline/
                      proc: 20
                      aligner: tophat2
                      genome: mouse
                      strand:

Once these paramenters are specified in detail, the pipeline is ready to run.

###Usage:
       
  

         python ./src/complete_seq.py -p {config file}.yaml
