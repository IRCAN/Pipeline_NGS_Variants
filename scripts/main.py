from Separation_transcripts import main_separation_transcripts
import os

"""
Script principal du pipeline qui traite le fichier .vcf de chaque patients d'un run
afin d'obtenir un compte rendu de mutations.

Ludovic KOSTHOWA (06/04/16)
"""



def read_file(File):
	"""Ouvre et lit le fichier .vcf de chaque patients."""
	contentFile = File.readlines()
	File.close() 
	return contentFile

def file_to_list(contentFile):
	"""Cree une liste contenant toutes les lignes du fichier .vcf.
	Chaque ligne est une liste composee d'elements (chrom,ID,position,etc)."""
	liste=[]
	for k in contentFile:
		liste.append(k)
	liste2liste=[]
	for k in liste:
		lignesplit = k.split('\t')
		liste2liste.append(lignesplit)
	return liste2liste

def output_file(FileName, Final_List):
	"""Cree un fichier resultat et ecrit dans ce fichier."""
	NomFile = FileName
	File = open(NomFile,'w')	# creation et ouverture du File
	for j in listeLegendes:		#ecriture de la legende
		j = "".join(j)
		File.write(str(j))
	for i in Final_List:	#ecriture des donnees
		File.write(str(i))
	File.close()

def check_if_multiple_id(listOfList):
	"""Regarde sur fichier original si plusieurs ID cosmic sur meme ligne
	si plusieurs ID, recupere les lignes separees dans ListdeNewLignes.
	Verifie en meme temps si la ligne correspond a une mutation et ajoute
	cette ligne dans une liste si c'est le cas. """
	contentNewVFC = []
	cmpt = 0
	for i in listOfList:
		ligne = i[2].split(";")
		if len(ligne) == 1:
			"""
			if "AF=0;AO=" in i[7]: #verifie si presence de mutation
				continue
			else:
				i="\t".join(i)
				contentNewVFC.append(i)"""
			i="\t".join(i)
			contentNewVFC.append(i)
		else:
			temp = []
			for j in ListdeNewLines[cmpt]:
				"""if "AF=0;AO=" in j[7]:	#verifie si presence de mutation
					continue
				else:
					j="\t".join(j)
					contentNewVFC.append(j)"""
				j="\t".join(j)
				contentNewVFC.append(j)		
			cmpt+=1
	return contentNewVFC	

def find_HSnm(lignes,hotspots):
	"""Compare les transcripts du fichier avec le fichier liste_hotspots
	et ressort les hotspots non mutes."""
	#je recupere tout les FAO = 0
	nonMuteHs = []
	for l in lignes:
		if "FAO=0;" in l:
			l = l.split("\t")
			for hs in hotspots:
				if l[0] == hs[0] and int(hs[1]) <= int(l[1]) <= int(hs[2]):
					listTemp=[]
					listTemp.append(hs[3])
					listTemp.append(hs[4])
					if listTemp in nonMuteHs : 
						continue
					else:
						nonMuteHs.append(listTemp)
	#print('Hotspots non mutés: ',nonMuteHs)
	return nonMuteHs

##############################################################
########					MAIN					  ########
##############################################################

#Ouverture fichier liste_HS
hs = "../Data/Thibault/liste_hotspots_TF.tsv"
hotspots_file = open(hs,'r')
hotspots_temp = read_file(hotspots_file)
hotspots = file_to_list(hotspots_temp)

#//TODO A modifier lorsque arborescence finale connue
#fichiers = ['TSVC_variants_IonXpress_002.vcf']
#,'TSVC_variants_IonXpress_002.vcf','TSVC_variants_IonXpress_005.vcf','TSVC_variants_IonXpress_006.vcf','TSVC_variants_IonXpress_007.vcf','TSVC_variants_IonXpress_008.vcf','TSVC_variants_IonXpress_009.vcf','TSVC_variants_IonXpress_012.vcf','TSVC_variants_IonXpress_013.vcf','TSVC_variants_IonXpress_016.vcf']
barecode = ['IonXpress_001','IonXpress_002','IonXpress_003','IonXpress_004','IonXpress_005','IonXpress_006','IonXpress_007','IonXpress_008','IonXpress_009','IonXpress_011','IonXpress_012','IonXpress_013','IonXpress_015','IonXpress_016',]
#//TODO FINAL: recuperer liste des  fichiers VCF du run en cours et boucler dessus

#####//TODO verifier si le dossier existe deja, si oui, ne pas le creer, si non le creer
os.mkdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/")
os.mkdir("../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/")
for i in barecode:
	fichier = 'TSVC_variants_'+i+'.vcf'
	#//TODO A modifier lorsque arborescence finale connue
	j = "../Data/Run_test/Auto_user_INS-80-TF_23-02-16_151_198/plugin_out/variantCaller_out.411/"+i+'/'+fichier
	print('Traitement du fichier: ',j)
	File = open(j,'r')
	contentFile = read_file(File)
	#Cree une liste avec chaque elements correspondant a une ligne du fichier
	listOfList = file_to_list(contentFile)
	#Supprime les informations inutiles du fichier VCF
	listeLegendes = listOfList[0:71]
	listeLegendes[70] = "\t".join(listeLegendes[70])
	del listOfList[0:71]
	del contentFile[0:71]
	#Appel de la fonction qui separe les transcripts presents sur la meme ligne
	ListdeNewLines = main_separation_transcripts(contentFile)
	#Traitement de la liste et ecriture dans fichier VCF: recupere les lignes avec 1 seul ID
	# dans listOfList et les autres dans ListdeNewLines + ajf_oute seulement les mutations
	list_of_transcripts = check_if_multiple_id(listOfList)
	#print(list_of_transcripts)
	#//TODO A modifier lorsque arborescence finale connue
	
	f_out = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/SEP_LIGNES_"+fichier
	#creation du fichier de sortie: fichier VCF avec un transcript par ligne
	output_file(f_out,list_of_transcripts)
	print('création de ',f_out)
	#print(list_of_transcripts)
	HSNONMUTE = find_HSnm(list_of_transcripts,hotspots)
	list_of_mutations = []
	for l in range(len(list_of_transcripts)):
		a = list_of_transcripts[l].split('\t')
		if "FAO=0;" not in a[7]:
			list_of_mutations.append(list_of_transcripts[l])
	f_out2 = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
	output_file(f_out2,list_of_mutations)
	print('création de ',f_out2)
	#suppression des FAO = 0
	#Pour chaque FAO != 0:
	
	#regarde dans HS si il en fait parti ????
	#lancer vep
	#recup id cosmic et comparer à HS et variants NGS
print("Fichier lignes separees crees !")
#//TODO prendre chaque FAO = 0 et comparer si ds HS


#verifie si le genome en local correspond a la derniere version du genome sur ensembl
os.system('rsync -u rsync://ftp.ensembl.org/ensembl/pub/current_variation/VEP/homo_sapiens_vep_84_GRCh38.tar.gz ../Data/Ensembl/')
for i in barecode:
	fichier = 'TSVC_variants_'+i+'.vcf'
	#//TODO faire la fonction dans script VEP + comparer resultats fichier debut et fichier fin
	inputfile = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VariantCaller/MUTATIONS_"+fichier
	output_file = "../Resultats/VEP/VEP_GAEL_"+fichier
	output_file1 = "../Resultats/VEP/VEP_LUDO_"+fichier
	output_file2 = "../Resultats/Auto_user_INS-80-TF_23-02-16_151_198/VEP/VEP_"+fichier
	#gael = mieux que script perso , + d'informations
	command = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl  -cache --no_stats --pick --refseq --symbol --hgvs --gmaf --sift b --polyphen b --canonical --regulatory --numbers --filter_common --filter coding_change,splice,regulatory --input_file "+inputfile+ " --output_file "+output_file
	#perso
	command2 = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl --appris --biotype --no_stats --check_existing --gmaf --maf_1kg --maf_esp --maf_exac --polyphen both --pubmed --regulatory --sift both --species homo_sapiens --symbol --tsl --cache --input_file "+inputfile+ " --output_file "+output_file1
	#test mix commande
	command3 = "perl ../Logiciels/ensembl-tools-release-84/scripts/variant_effect_predictor/variant_effect_predictor.pl -cache --no_stats --symbol --sift b --hgvs --gmaf --polyphen b --regulatory --filter_common --biotype --pubmed --input_file "+inputfile+ " --output_file "+output_file2
	#os.system(command)
	#os.system(command2)
	os.system(command3)
print("Creation fichiers par VEP OK")

##//TODO realiser intersection avec fichiers tibo