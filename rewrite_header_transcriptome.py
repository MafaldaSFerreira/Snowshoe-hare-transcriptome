#This is a programe that subtitutes the "contig###" code by the original
#header of the transcriptome (Trinity output) based on a correspondence file
#correspondance tab delimited file with component code in first column and contig code in
#the second column.
#AUTHOR: Mafalda Sousa Ferreira 10NOV2014@Porto
#USAGE: python rewrite_header_transcriptome.py correspondence.txt in_transcriptome out_transcriptome

import sys

mycorrespondence=sys.argv[1]
myintranscriptome=sys.argv[2]
myouttranscriptome=sys.argv[3]

def changeheader(correspondence,intranscriptome,outtranscriptome):
	mycorr=open(correspondence,'r')
	intransc=open(intranscriptome,'r')
	outtrans=open(outtranscriptome,'w')
	corrdict={}
	
	for line in mycorr:
		myfield=line.split('\t')
		mycomp=myfield[0]
		mycontig=''.join(myfield[1].split())
		#print mycomp, mycontig
		corrdict.setdefault(mycontig,mycomp)
	#print corrdict
	
	for line in intransc:
		if line.startswith('>'):
			myfield=line.split(' ')
			#print myfield
			mycontig=''.join(myfield[0].split())
			#print mycontig
			if mycontig in corrdict:
				mycomp=corrdict[mycontig]
				#print mycomp
				myheader=''.join(mycomp+' '+myfield[1].strip()+' '+mycontig.strip('>')+'\n')
				myline=myheader
				#print myline
				outtrans.write(myline)
			else:
				print "WARNING"
		else:
			outtrans.write(line)
	
	outtrans.close()			
	return			

#Call the function	
changeheader(mycorrespondence,myintranscriptome,myouttranscriptome)
