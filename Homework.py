import math

def mediaR(medie):
	risultato = []
	for media in medie:
		risultato.append(media / medie[0])
	return risultato

def ricorrenza(misure): #crea lista di blocked data
	misureIterazione= []
	for t in range (0,(len(misure))/2):
		u1= 0.5* (misure[(2*t)-1][1]+misure[2*t][1])
		u2= 0.5* (misure[(2*t)-1][2]+misure[2*t][2])
		tupla=(t, u1, u2)
		misureIterazione.append(tupla)
	#print len(misureIterazione)
	return misureIterazione

def mediaErrore(misure): #calcola media ed errore
	#medie scorrelate
	sommau1=0.0
	sommau2=0.0
	for misura in misure:
		sommau1 += misura[1]
		sommau2 += misura[2]
	numRighe=len(misure)
	media1=sommau1/numRighe
	media2=sommau2/numRighe
	#sigma scorrelate
	valMedQuadr1=0.0 #calcola il valore medio dei quadrati
	valMedQuadr2=0.0
	for misura in misure:
		valMedQuadr1 += misura[1]**2
		valMedQuadr2 += misura[2]**2
	sigmaquadro1 = ((valMedQuadr1/numRighe)-(media1**2))/(numRighe-1) #calcola sigma quadro
	sigmaquadro2 = ((valMedQuadr2/numRighe)-(media2**2))/(numRighe-1)
	sigma1= math.sqrt(sigmaquadro1) #calcola sigma
	sigma2= math.sqrt(sigmaquadro2)
	return (media1, sigma1, media2, sigma2)

def autocorrelazione(misure, k, media1, media2):
	autoCorr1=0.0
	autoCorr2=0.0
	for j in range (0,len(misure)-k):
		autoCorr1+= (misure[j+k][1]-media1)*(misure[j][1]-media1)
		autoCorr2+= (misure[j+k][2]-media2)*(misure[j][2]-media2)
	C1= (1.0/(len(misure)-k))*autoCorr1
	C2= (1.0/(len(misure)-k))*autoCorr2
	#print autoCorr1
	#print autoCorr2
	return (C1,C2)

def autocorrAnalysis(misure, media1, media2, nomeFile):
	k1=0
	k2=0
	k=0
	Trovato1=False
	Trovato2=False
	CK1=[]
	CK2=[]
	while ((not Trovato1 or not Trovato2) or (k<200)):
		ktemp1, ktemp2= autocorrelazione(misure, k, media1, media2)
		CK1.append(ktemp1)
		CK2.append(ktemp2)
		if ktemp1 < 0 and not Trovato1:
			k1= k-1
			Trovato1 = True
		if ktemp2 < 0 and not Trovato2:
			k2= k-1
			Trovato2 = True
		k +=1
	C01=CK1[0]
	C02=CK2[0]
	tauint1=0.0
	tauint2=0.0
	for k in range(1, k1):
		tauint1 += CK1[k] / C01
	for k in range(1, k2):
		tauint2 += CK2[k] / C02
	tauint1 += 0.5
	tauint2 += 0.5
	sigma1= math.sqrt((C01/len(misure))*2*tauint1)
	sigma2= math.sqrt((C02/len(misure))*2*tauint2)
	with open('autocorrAnalysis.'+nomeFile, 'w') as the_file:
		the_file.write(str(CK1))
		the_file.write('\n ----- \n')
		the_file.write(str(CK2))
	return(k1, tauint1, sigma1, k2, tauint2, sigma2)


def blockedJacknife(misure):
	inizio=0
	fine=2000
	blocked2000=[]
	for indice in range(0,50):
		blocked2000.append(misure[inizio:fine])
		inizio += 2000
		fine += 2000
	return blocked2000

#def rapporto(blockedJ):


def Homework(nomeFile):
	misureMC=[] #crea contenitore tuple misure
	righe=[] #crea lista vuota per le righe
	with open(nomeFile, 'U') as f: #apre file
		data=f.read() #copia in una stringa tutto il documento
		righe=data.split('\n') #divide in righe
	for riga in righe:
		elementi=riga.split(' ') #separa gli elementi in ogni riga
		tempo=int(elementi[0]) #assegna il tipo a ogni elemento
		u1=float(elementi[1])
		u2=float(elementi[2])
		tupla= (tempo, u1, u2)
		misureMC.append(tupla) #riempie il contenitore di tuple
	#medie ed errori scorrelati
	media1, sigma1, media2, sigma2 = mediaErrore(misureMC)
	with open('mediaErroreScorr.'+nomeFile, 'w') as the_file: #stampa media ed errori scorrelati
		the_file.write('media \n')
		the_file.write(str(media1))
		the_file.write('\nerrore \n')
		the_file.write(str(sigma1))
		the_file.write('\n ----- \n')
		the_file.write('media \n')
		the_file.write(str(media2))
		the_file.write('\nerrore \n')
		the_file.write(str(sigma2))
	#genera blocked data
	blockedData= []
	ultimaRicorrenza=misureMC
	sigma1B= []
	sigma2B= []
	media1B= []
	media2B= []
	while len(ultimaRicorrenza)>3: #dimensione ultimo blocco
		ultimaRicorrenza= ricorrenza(ultimaRicorrenza)
		blockedData.append(ultimaRicorrenza)
		#medie ed errori blocked data
		a, b, c, d = mediaErrore(ultimaRicorrenza)
		media1B.append(a)
		sigma1B.append(b)
		media2B.append(c)
		sigma2B.append(d)
	with open('mediaErroreBlocked.'+nomeFile, 'w') as the_file: #stampa media ed errori Blocked
		the_file.write(str(media1B))
		the_file.write('\n errore \n')
		the_file.write(str(sigma1B))
		the_file.write('\n ----- \n')
		the_file.write(str(media2B))
		the_file.write('\n errore \n')
		the_file.write(str(sigma2B))
	#autocorrelation analysis
	#print autocorrelazione(misureMC, , media1, media2)
	ktausigma=autocorrAnalysis(misureMC, media1, media2, nomeFile)
	with open('kTauSigmaAutocorr.'+nomeFile, 'w') as the_file: #stampa tupla k, tau, sigma
		for valore in ktausigma:
			the_file.write(str(valore))
			the_file.write('\n')

	print '----------'
	return (misureMC, [ktausigma[2], ktausigma[5]], [media1, media2])

def mediaJK(blocco, u): #calcola la media su una colonna di un blocco
	media=0.0
	for misura in blocco:
		media += misura[u]
	media = media/len(blocco)
	return media

def generaMatrMedieJK(matrMedie):
	matrMedieJK=[]
	for indiceRiga in range(0,len(matrMedie)):
		matrMedieJK.append(uHat(matrMedie, indiceRiga))
	return matrMedieJK

def uHat(blocco, indice): #calcola la media JK per le Ui medie
	sommaU1=0.0
	sommaU2=0.0
	sommaU3=0.0
	sommaU4=0.0
	for k in range (0,len(blocco)):
		if k==indice:
			continue
		sommaU1 += blocco[k][0]
		sommaU2 += blocco[k][1]
		sommaU3 += blocco[k][2]
		sommaU4 += blocco[k][3]
	mediaJK1= sommaU1/(len(blocco)-1.0)
	mediaJK2= sommaU2/(len(blocco)-1.0)
	mediaJK3= sommaU3/(len(blocco)-1.0)
	mediaJK4= sommaU4/(len(blocco)-1.0)
	return [mediaJK1, mediaJK2, mediaJK3, mediaJK4]

def ratioI(matrMedie):
	rapportiParziali=[]
	for riga in matrMedie:
		rapportiParzialiTemp=[]
		for colonna in range(0,4):
			rapportiParzialiTemp.append(riga[colonna]/riga[0])
		rapportiParziali.append(rapportiParzialiTemp)
	return rapportiParziali

def sigmaRJK(rapportiParziali, rAve):
	sigmaRJK1=0.0
	sigmaRJK2=0.0
	sigmaRJK3=0.0
	sigmaRJK4=0.0
	nmunofratton = ((len(rapportiParziali)-1.0)/len(rapportiParziali))
	for riga in rapportiParziali:
		sigmaRJK1 += (riga[0] - rAve[0])**2
		sigmaRJK2 += (riga[1] - rAve[1])**2
		sigmaRJK3 += (riga[2] - rAve[2])**2
		sigmaRJK4 += (riga[3] - rAve[3])**2
	sigmaRJK1= math.sqrt(sigmaRJK1*nmunofratton)
	sigmaRJK2= math.sqrt(sigmaRJK2*nmunofratton)
	sigmaRJK3= math.sqrt(sigmaRJK3*nmunofratton)
	sigmaRJK4= math.sqrt(sigmaRJK4*nmunofratton)
	return [sigmaRJK1, sigmaRJK2, sigmaRJK3, sigmaRJK4]

file1, kTauSigmaAutocorr1, medieFile1 =Homework('data1.txt')
file2, kTauSigmaAutocorr2, medieFile2 =Homework('data2.txt')

medie = medieFile1 + medieFile2
autocorrSigma = kTauSigmaAutocorr1 + kTauSigmaAutocorr2

#print autocorrSigma

jacknifeCompleto= []
for misura1, misura2 in zip(file1, file2): #fonde i due file di dati in uno
	jacknifeCompleto.append((misura1[0], misura1[1], misura1[2], misura2[1], misura2[2]))
#print jacknifeCompleto[0]
jacknifeDataBlock2000=blockedJacknife(jacknifeCompleto) #scrive un file con 5 colonne (t, U1, U2, U3, U4)

with open('jacknifeDataBlock2000.txt', 'w') as the_file: #stampa i tre rapporti in riga
	the_file.write('Fusione data1, data 2:\n')
	for blocco in jacknifeDataBlock2000:
		the_file.write(str(blocco))
		the_file.write('\n \n \n \n')

medieBlocked=[] #restituisce le medie di tutti i blocchi per ogni colonna
for blocco in jacknifeDataBlock2000:
	arrayValMedBlocco=[]
	for u in range (1,5):
		arrayValMedBlocco.append(mediaJK(blocco, u))
	medieBlocked.append(arrayValMedBlocco)

with open('matriceMedieUi.txt', 'w') as the_file: #stampa matrice 50*4 con le medie aritmetiche Ui
	the_file.write('Matrice 50*4 con le medie arimetiche di Ui:\n')
	for riga in medieBlocked:
		the_file.write(str(riga))
		the_file.write('\n\n')
#print medieBlocked --> stampa 50 liste ciascuna delle quali contiene le 4 medie aritmetiche delle Ui
#print generaMatrMedieJK(medieBlocked) matrice 50*4 con UiJK
matrMedieJK=generaMatrMedieJK(medieBlocked)
with open('matriceMedieJK.txt', 'w') as the_file: #stampa matrice 50*4 con UiJK
	the_file.write('Matrice 50*4 con le medie JK di Ui:\n')
	for riga in matrMedieJK:
		the_file.write(str(riga))
		the_file.write('\n\n')

mediaAritmUi=[] #calcoliamo le medie aritmetiche delle medie JK di Ui
for i in range(0,4):
	mediaAritmUi.append(mediaJK(matrMedieJK, i))
with open('MedieAritmUiJK.txt', 'w') as the_file: #stampa medie aritmetiche delle UiJK
	the_file.write('Medie aritmetiche delle medie JK di Ui:\n')
	the_file.write(str(mediaAritmUi))

aritmU1=mediaAritmUi[0]
ratioAritmUi=[]
for indice in range(0,4):
	ratioAritmUi.append((mediaAritmUi[indice])/aritmU1)

#print ratioAritmUi

with open('ratioUi.txt', 'w') as the_file: #stampa Ri
	the_file.write('Rapporti medie Ui:\n')
	the_file.write(str(ratioAritmUi))

rapportiParziali=ratioI(matrMedieJK)
with open('rapportiParziali.txt', 'w') as the_file:
	the_file.write('Rapporti parziali:\n')
	for riga in rapportiParziali:
		the_file.write(str(riga))
		the_file.write('\n')


erroreJK=sigmaRJK(rapportiParziali, ratioAritmUi)

#print erroreJK

with open('erroriJK.txt', 'w') as the_file:
	the_file.write('Errori JK sulle R:\n')
	the_file.write(str(erroreJK))

#mediaIEF1=mediaJK(medieBlocked, 0)
medieR = mediaR(medie)


indepErrorFormula = []
for colonna in range(0,4):
	#print medieR[colonna]
	#print autocorrSigma[colonna]
	#print medie[colonna]
	rQuadro = medieR[colonna]**2
	ratioTemp = (autocorrSigma[0]**2/medie[0]**2)
	ratioTemp += (autocorrSigma[colonna]**2/medie[colonna]**2)
	ratioTemp *= rQuadro
	ratioTemp = math.sqrt(ratioTemp)

	indepErrorFormula.append(ratioTemp)
#print indepErrorFormula

with open('erroriIEF.txt', 'w') as the_file: #stampa gli errori IEF
	the_file.write('Errori IEF sulle R:\n')
	the_file.write(str(indepErrorFormula))

worstErrorFormula = []
for colonna in range(0,4):
	rQuadro = medieR[colonna]**2
	ratioTemp = autocorrSigma[0]/abs(medie[0])
	ratioTemp += autocorrSigma[colonna]/abs(medie[colonna])
	ratioTemp *= ratioTemp
	ratioTemp *= rQuadro
	ratioTemp=math.sqrt(ratioTemp)
	worstErrorFormula.append(ratioTemp)
#print worstErrorFormula

with open('erroriWEF.txt', 'w') as the_file: #stampa gli errori WEF
	the_file.write('Errori WEF sulle R:\n')
	the_file.write(str(worstErrorFormula))
