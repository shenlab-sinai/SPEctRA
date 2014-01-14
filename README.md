Complete-Seq RNAseq Pipeline:
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
     
######[Please refer to this example configuration YAML file:](../src/config_template.yaml)
          
- The `Environment` header corresponds to the linux shell environment where you are submitting pipeline-generated jobs. This could either be a  `cluster` such as Minerva or a `server` like ngseq/gwas/medinfo
- The `project_directory` header specifies the absolute path to a directory where you wish to save <i>all</i> your pipeline-run tasks. Each task will be separated in subdirectories outlined in the [Job execution file](pipeline_start_template.yaml)
           
Short-read_aligners:
            tophat2: tophat/2.0.9
            bowtie2: bowtie2/2.1.0
            STAR: rna-star/2.3.0e
           genomes:
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
     

  6. Usage:
       


         python ./src/complete_seq.py -p {config file}.yaml
