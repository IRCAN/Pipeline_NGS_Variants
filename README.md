![Logo IRCAN](http://ircan.org/images/stories/logo_ircan.png)

# Pipeline_NGS_Variants Project

### By Ludovic Kosthowa (Intern Master student)
### During 6 month internship
### Created 15/02/2016

---
__Informations :__

This project is not finished. I'm currently working on this project so all code could be changed.
Thank you for your understanding.

---

Workspace of created pipeline for variants NGS analysis:
	This pipeline is used to find and annotate variants from the Ion PGM.
	This pipeline runs on each analysis made with the PGM.
	It can be adapted to different research subject.

__Quick Start :__

Download VarAn (green button, in top rigth) in zip format or by using *git clone* command.

Extract and go in the scripts repertory. Open the terminal and write:

```
cd your/path/to/the/repertory/Pipeline_NGS_Variants/scripts
```

Run the installLog.sh with this command
```
sudo bash installLog.sh
```
Follow the instructions. You must to download the Human Grch37 data from VEP by choosing __43 45__ when it's prompt. Do the same thing for the Human genome fasta file by writing __27__ .

You also need to download ["CosmicCompleteExport.tsv"](http://cancer.sanger.ac.uk/cell_lines/files?data=/files/grch37/cosmic/v75/CosmicCompleteExport.tsv.gz) from Cosmic database. Follow the instructions on the link. 

After the download, don't forget to put and extract the file in the System/Cosmic/ repertory.

Now, you can run VarAn with the command below:
```
python3 varan.py Path_to_the_run_repertory/
```

__Repository :__
- "__scripts__" contain all python3 scripts.

- "__Results__" contain output file created by scripts.

- "__Personal_Data__" contain personal files like hotspots files or panel list.

- "__System__" contain files needed to launch the software.

- "__System/Cosmic__": repository of Cosmic database with Complete and Lite database. If you download the git repository for the first time, you need to download the ["CosmicCompleteExport.tsv"](http://cancer.sanger.ac.uk/cell_lines/files?data=/files/grch37/cosmic/v75/CosmicCompleteExport.tsv.gz) from Cosmic database. Follow the instructions on the link. After the download, don't forget to put the file in the Cosmic repertory.

- "__System/Ensembl__": repository of Ensembl tools (VEP script and database). If you download the git repository for the first time, you need to download the  ["homo_sapiens_vep_84_GRCh37.tar.gz"](http://ftp.ensembl.org/pub/current_variation/VEP/homo_sapiens_vep_84_GRCh37.tar.gz) from ensembl website.

__Documentations :__

Documentation of this pipeline is in "__html__" repository.
Documentation made with epydoc.

__Contributors :__

* [Ludovic Kosthowa](https://github.com/LudoKt), Master student.
* Florent Tessier, IRCAN, Cancéropôle.
