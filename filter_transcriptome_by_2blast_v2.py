#This is a program that will join the contig code and ENSEMBL gene code
#from two blast results (Oryc and Mus) into one single dictionary 
#and will create a new transcriptome fasta file only with the contigs
#that were annotated in the Oryc or Mus database.
#version 2 outputs the header of the transcriptome as it was plus the annotation
#The transcriptome header was this: contig#####; where ##### is a unique number. 
#I reinstituted the original Trinity codes a posteriori.
#Done by Mafalda SFerreira 9 Nov 2014 @ Rechousa
#USAGE:python filter_transcriptome_by_2blastx_v2.py blast_output_file1 blast_output_file2 transcriptome output_file

import sys

myblast_file1=sys.argv[1]
myblast_file2=sys.argv[2]
mytranscriptome=sys.argv[3]
myoutfile=sys.argv[4]

def makeblastdict(myblastfile1,myblastfile2):
#def makeblastdict(myblastfile1):
	mydict1={}
	mydict2={}
	mydictf={} #the final dictionary that will be the result of both
	objblastfile1=open(myblastfile1,'r')
	
	for myline in objblastfile1:
		if not myline.startswith('c'): #because the first line might not start with c depending on the blast result
			pass
		else:
			myfields=myline.strip().split("\t")
			myids=(myfields[1]).split("|")
			mygene=myids[1].split('\n')
			mygene=''.join(mygene)      #change mycontig from a list type to a string since dic does not accept lists (mutable)
			mycontig=myfields[0].split('\n')
			mycontig=''.join(mycontig)  
			#print mycontig
			mydict1.setdefault(mycontig,mygene)
	#print mydict1, '\n-----------------------------------------------------------------------\n'
			#mydict1[mycontig]=myfields[0]   
	#print mydict1
	#end for
	
	objblastfile2=open(myblastfile2,'r')
	for myline in objblastfile2:
		if not myline.startswith('c'):
			pass
		else:
			myfields=myline.strip().split("\t")
			myids=(myfields[1]).split("|")
			mygene=myids[1].split('\n')
			mygene=''.join(mygene)
			mycontig=myfields[0].split('\n')
			mycontig=''.join(mycontig)
			mydict2.setdefault(mycontig,mygene)
			
	#print mydict1, '\n-------------------------------\n', mydict2

	#making the final dictionary
	keys1=mydict1.keys()
	#print keys1
	for key1 in keys1:
		if key1 in mydict2:
			gene1=mydict1.get(key1)
			gene2=mydict2.get(key1)
			#print gene1, gene2
			genef=''.join(gene1+'|'+gene2)
			mydictf.setdefault(key1,genef)
		elif key1 not in mydict2:
			gene3=mydict1.get(key1)
			#print gene3
			mydictf.setdefault(key1,gene3)
	
	keys2=mydict2.keys()
	#print keys2
	for key2 in keys2:
		if key2 not in mydict1:
			gene4=mydict2.get(key2)
			#print gene4
			mydictf.setdefault(key2,gene4)
		
	return mydictf

#makeblastdict('sample_blast_1','sample_blast_2')	

##Calling my function
#Outputfile	
outfile=open(myoutfile,'w')
#outfile=open('output_test2.fasta','w')
#Transcriptome
transcriptomefile=open(mytranscriptome,'r')
#transcriptomefile=open('ameskin.Trinity.contig.lin.fasta','r')
#Blast results and making the dictionary
mymaindict=makeblastdict(myblast_file1,myblast_file2)
#mymaindict=makeblastdict('sample_blast_1','sample_blast_2')

doprint=False
for myline in transcriptomefile:
	if myline.startswith('>'):
		myids=myline.strip('>')
		mycontigs=myids[0:].strip()
		if mycontigs in mymaindict:		
			doprint=True
			myheader=''.join(myline.strip()+'\t'+mymaindict[mycontigs]+'\n')
			#print myheader
			outfile.write(myheader)
		else:
			doprint=False
			pass
	else:
		if doprint==True:  #it needs to be '==' because now we are making a question! not only changing the value of doprint
			#print myline,
			outfile.write(myline)

outfile.close()
transcriptomefile.close()
sys.exit()
			