#!/usr/bin/python
# coding: utf-8 
import re

"""
Script pour separer une ligne du fichier VCF
composee de plusieurs transcripts en plusieurs
lignes: une ligne par transcript.

Ludovic KOSTHOWA (06/04/16)
"""

class SeparationVariants:

	########	Variable(s)	########
	def __init__(self):
		self.LEGENDES = ['AF=','AO=','DP=','FAO=','FDP=','FR=','FRO=','FSAF=','FSAR=','FSRF=','FSRR=','FWDB=','FXX=','HRUN=','LEN=','MLLD=','OALT=','OID=','OMAPLAT=','OPOS=','OREF=','QD=','RBI=','REFB=','REVB=','RO=','SAF=','SAR=','SRF=','SRR=','SSEN=','SSEP=','SSSB=','STB=','STBP=','TYPE=','VARB=','']
	########	Fonctions	########

	def read_file(self,File):
		"""Ouvre et lit le fichier .vcf de chaque patients."""
		contentFile = File.readlines()
		File.close()
		return contentFile

	def check_if_multiple_ID(self,contentFile):
		"""Cree une liste composee seulement des lignes possedants plusieurs
		mutations. """
		contentFileList=[]
		for k in contentFile:
			contentFileList.append(k)
		listOflist=[]
		for k in contentFileList:
			lignesplit = k.split('\t')
			listOflist.append(lignesplit)
		cpt = 0
		multipleIDList = []
		for i in listOflist:
			ligne = i[4].split(",")
			#Si il y a plus (+) que une seule mutations, je cree une liste de ces ID.	
			if len(ligne) != 1:
				multipleIDList.append(contentFile[cpt])
			cpt += 1
		return multipleIDList

	def create_list_of_list(self,contentFile):
		"""Cree pour chaque ligne une liste de toutes les informations des
		differents identifiants cosmics. Cette liste est ajoutee dans une liste globale.
		Cette fonction permet de separer tout les elements necessaires a la
		separation des lignes composees de plusirs ID cosmics."""
		listContentFile = [] #liste du contenu du fichier
		#separation de contentFile par les tabulations!
		listFinale =[]
		for element in contentFile:
			contentFile = element.split('\t')
			listContentFile.append(contentFile)
		for ligneChromosome in listContentFile:
			listLigneTemp = [] #liste temporaire correspondant a une ligne (1 transcript)
			listInfoTemp = []	#liste de la cellule INFO du fichier VCF
			listLigneInfoTrie = []	#liste finale correspondant aux informations triees pour chaque transcript
			for element in ligneChromosome:
				#separation de contentFile par les ";"
				if ";" in element:
					temp = element.split(";")
					listInfoTemp.append(temp)
				#separation de contentFile par les ","
				elif "," in element:
					temp = element.split(",")
					listInfoTemp.append(temp)
				else:
					listInfoTemp.append(element)
			#traitement et separations des informations de la cellule INFO
			listInfoTemp[7][5] = listInfoTemp[7][5].replace(",","")
			for element in listInfoTemp[7]:
				listLigneTempElement7 = element.split(",")
				listLigneInfoTrie.append(listLigneTempElement7)
			for element in listInfoTemp:
				if type(element) != list:
					listLigneTemp.append(element)
				elif type(element) == list:
					if element == listInfoTemp[7]:
						listLigneInfoTrie = []
						for element in listInfoTemp[7]:
							listLigneTempElement7 = element.split(",")
							listLigneInfoTrie.append(listLigneTempElement7)
						listLigneTemp.append(listLigneInfoTrie)	
					else:
						listLigneTemp.append(element)
			#verification pour eviter saut de ligne dans fichier VCF
			if "\n" in listLigneTemp[-1]:
				listLigneTemp[-1] = listLigneTemp[-1].replace("\n","")
				listFinale.append(listLigneTemp)
			else:
				listFinale.append(listLigneTemp)
		return listFinale

	def trie_informations(self,listLigneTemp):
		"""Suppression des legendes (FAO,AF,AO,...) 
		par recherche d'une expression reguliere."""
		for i in listLigneTemp[7]:
			temp = str(i[0])
			temp = re.sub(r"([A-Z])+=","",temp)
			i[0] = temp

	def check_if_same_length(self,listLigneTemp):
		"""Verifie si la ligne possede le meme nombre d'ID cosmic
		que de mutations."""
		#nombre d'elements de la cellule INFO
		cmpt = len(listLigneTemp[7])
		newLines = []
		compteurID= 0
		#Pour chaque ligne , je cree une liste que je mets dans newLines
		#Verification si meme nombre ID cosmic que nombre de mutations
		if len(listLigneTemp[2]) == len(listLigneTemp[4]):
			nbeBoucle = 4
			self.creation_lignes(listLigneTemp,cmpt,compteurID,newLines,nbeBoucle)
		else:
		#boucle sur le plus petit element
			#boucle sur ID cosmic
			if len(listLigneTemp[2]) < len(listLigneTemp[4]):
				nbeBoucle = 2
				self.creation_lignes(listLigneTemp,cmpt,compteurID,newLines,nbeBoucle)
			#boucle sur le nombre de mutations (/!\ Possible perte du dernier ID cosmic)
			else:
				nbeBoucle = 4
				self.creation_lignes(listLigneTemp,cmpt,compteurID,newLines,nbeBoucle)
		return newLines

	def creation_lignes(self,listLigneTemp,cmpt,compteurID,newLines,a):
		"""Recupere les informations correspondants a chaque ID cosmic
		et cree une nouvelle ligne avec ces informations."""
		#pour chaque elements de la liste, recuperation des informations
		for i in range(len(listLigneTemp[a])):
			ligneTemp = []
			for element in listLigneTemp:
				# Si c'est une string, on ajoute dans listLigneTemp.
				if type(element) == str:
					ligneTemp.append(element)
				# Si c'est une liste, on on traite chaque elements de la liste
				if type(element) == list:
					if type(element[compteurID]) == str:
						ligneTemp.append(element[compteurID])
					else:
						#boucle sur la longueur de la cellule info pour extraire chaque donnees
						for number in range(cmpt):
							if len(element[number]) == 1:
								#uniformisation du contenu de la liste
								temp = str(element[number])
								temp = temp.replace("[","")
								temp = temp.replace("]","")
								temp = temp.replace("'","")
								temp = self.LEGENDES[number]+temp
								ligneTemp.append(temp)
							else:
								temp = self.LEGENDES[number]+element[number][compteurID]
								ligneTemp.append(temp)
			#mise en forme comme VCF				
			listVCF = ligneTemp[:]
			del listVCF[7:]
			del ligneTemp[0:7]
			listTemptoString = ";".join(ligneTemp)
			listTemptoString += "\n"
			listVCF.append(listTemptoString)
			newLines.append(listVCF)
			#incrementation pour passer a un nouveau transcript de la meme ligne
			compteurID +=1
		return newLines


##############################################################
########					MAIN					  ########
##############################################################
#Fonction qui traite les lignes composees de plusieurs ID cosmic

def main_separation_variants(contentFile):
	"""Traite les lignes composees de plusieurs ID cosmic
	et cree de nouvelles lignes pour chaque identifiant.
	Retourne la liste des nouvelles lignes.

	@param	contentFile : contenu du fichier VCF
	@return listNewLines : liste des lignes ( un ID par ligne)."""
	sep=SeparationVariants()
	listNewLines = []
	contentFileCleaned = sep.check_if_multiple_ID(contentFile)
	listLigneTemp = sep.create_list_of_list(contentFileCleaned)
	
	for i in listLigneTemp:
		
		sep.trie_informations(i)
		newLines = sep.check_if_same_length(i)
		listNewLines.append(newLines)
	return listNewLines


