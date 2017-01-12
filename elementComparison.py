import io
import sys

import re

import os
import math


from operator import itemgetter

import Stemmer

import nltk
from nltk.corpus import stopwords


wordSpace = 0
idfVector = []

tfMatrix = []

fileNameVector = []
#fileContentVector = []

query = []


#dossier des documents
folder = "PolyHEC"

#type de documents
extension = ".txt"


queryFile = ""

stemmingFilter = True
stopWordsFilter = True



################################## FONCTIONS PRINCIPALES ##################################


#Calcul l'espace de mots pour un dossier de documents.
def getWordSpace():
    global wordSpace
    global folder
    global extension
    
    #Reinitialisation de la chaine
    wordSpaceString = ""
    
    #Creation d'une chaine contenant tous les mots de tous les documents
    for file in os.listdir(folder):
        if file.endswith(extension):
            file = folder + "/" + file
            wordSpaceString = wordSpaceString + " " + readFile(file)

    #Tri des mots pour ne conserver que ce qui est necessaire
    wordSpace = getIndividualWords(wordSpaceString)
    return wordSpace


#Fonction qui construit la matrice des termes dans tous les documents d'un dossier incluant le document constituant la requete. L'information
#est stockee dans la variable globale tfMatrix
def getTfMatrix():
    global wordSpace
    global tfMatrix
    global fileNameVector
    
    global folder
    global extension
    
    #recherche de tous les documents .txt dans le dossier folder
    for file in os.listdir(folder):
        if file.endswith(extension):
            
            #ajout du nom
            fileNameVector.append(file)
            
            #Lecture du fichier
            file = folder + "/" + file
            sentence = readFile(file)
            
            #Ajout du contenu
            #fileContentVector.append(sentence)
            
            #ajout du vecteur du document dans la matrice
            tfMatrix.append(getWordVector(sentence))
    
    return tfMatrix


#Fonction qui calcule le vecteur idf pour l'espace de mots. L'information est stockee dans idfVector
def getIdfVector():
    global wordSpace
    global tfMatrix
    global idfVector
    
    dfVector = [0] * len(wordSpace)
    
    #Compte dans combien de documents le mot est present
    for document in tfMatrix:
        for word in range(len(document)):
            if document[word] != 0:
                dfVector[word] = dfVector[word] + 1

    #Fait le calcul de l'inverse pour tous les elements du vecteur
    for j in dfVector:
        if j == 0:
            idfVector.append(0)
        else:
            idfVector.append( math.log(float(len(tfMatrix)) / float(j), 10) )

    return idfVector



#Fonction qui calcule le coefficient de similitude selon la methode du cosinus pour tous les documents.
#Un vecteur contenant les score et les noms des document est retourne
def getSimilitudeCoefficientsCosine(query):
    #global query
    global fileNameVector
    global tfMatrix
    keys = ['file', 'value']
    value = []
    
    queryLength = computeLength(query)
    
    for i in range(len(fileNameVector)):
        result = [fileNameVector[i],computeSimilitudeCoefficient(tfMatrix[i],query) / ( computeLength(tfMatrix[i]) * queryLength)]
        value.append(dict(zip(keys,result)))
    
    return value


################################## FONCTIONS PRINCIPALES ##################################


################################## FONCTIONS AUXILIAIRES ##################################

#Fonction qui tri un tableau data selon un item et qui conserve les number premiers elements
def sortData(number,data,item):
    result = []

    if number > len(data):
        number = len(data)
    #Tri
    data = sorted(data, key=itemgetter(item),reverse=True)

    #Conservation des premiers elements
    for i in range(number):
        result.append(data[i])

    return result


#Fonction qui lit le fichier file dans le dossier folder et retourne le contenu dans une chaine
def readElement(file):
    global folder
    
    sentence = readFile(folder + "/" + file)
    return sentence


#Fonction qui calcule le coefficient de similitude non normalise pour tous les documents.
#Un vecteur contenant les scores et les noms des document est retourne
def getSimilitudeCoefficients():
    global query
    global fileNameVector
    global tfMatrix
    keys = ['file', 'value']
    value = []
    
    for i in range(len(fileNameVector)):
        result = [fileNameVector[i],computeSimilitudeCoefficient(tfMatrix[i],query)]
        value.append(dict(zip(keys,result)))
    
    return value


#Fonction qui compare WordSpace a data. Le vecteur contenant le nombre d'occurences est retourne
def getWordVector(data):
    global wordSpace
    
    fdist = getIndividualWords(data)
    vector=[]
    
    for value in wordSpace.keys():
        vector.append(fdist[value])
    return vector

#Fonction qui lit une chaine de caracteres et compte les differentes occurences de mots. Par defaut, la ponctuation est enlevee
#et il est aussi possible de nettoyer la chaine en supprimant des mots vides (stopwords) et en radicalisant certains mots. Une structure
#contenant les mots et leur nombre est retourne
def getIndividualWords(data):
    
    #Activer ou non certains filtres
    global stopWordsFilter
    global stemmingFilter
    
    tokens = nltk.word_tokenize(data)
    
    #Supprime les stopwords
    if stopWordsFilter is True:
        stops = set(stopwords.words('french'))
        tokens = [word for word in tokens if word not in stops]
    
    #Supprime la ponctuation
    punct = ['?','!',';','.',',',':']
    tokens = [word for word in tokens if word not in punct]

    #Radicalise les mots
    if stemmingFilter is True:
        stemmer = Stemmer.Stemmer('french')
        tokens = stemmer.stemWords(tokens)
    
    #Fait le compte
    fdist = nltk.FreqDist(tokens)
    return fdist



#Fonction qui prend un nom de fichier texte en entree et en retourne le contenu. Les sauts de ligne sont remplacees
#par des espaces et les espaces a la fin sont enleves pour assurer que le compte soit bon meme si le dernier caractere est un saut de ligne
def readFile(file):
    
    try:
        result = open(file, 'r', encoding="utf8")
    except FileNotFoundError:
        print("Fichier non trouve!")
        return -1
    
    else:
        string = result.read().replace('\n',' ')
        string.rstrip()
        
        result.close()
        return string




#Fonction qui fait le produit scalaire entre le vecteur data et query. La valeur est retournee
def computeSimilitudeCoefficient(data,query):
    global idfVector
    result = 0
    
    for i in range(len(data)):
        result = result + idfVector[i]*idfVector[i]*float(data[i])*float(query[i])
    return result

#Fonction qui calcule la norme d'un vecteur data. La valeur est retournee
def computeLength(data):
    global idfVector
    result = 0
    
    for i in range(len(data)):
        result = result + idfVector[i]*idfVector[i]*data[i]*data[i]
    result = math.sqrt(result)
    return result




#Fonction qui formatte le contenu de data. Par defaut, les fichiers sont relus pour eviter de stocker une trop grande quantite d'info en memoire
def formatResponse(data):
    global folder
    
    request = []
    result = []
    keys = ['id','title','description']
    majorKeys = ['','']
    
    #Lecture de tous les elements
    for i in range(len(data)):
        
        file = folder + "/" + data[i]['file']
        
        sentence = readFile(file)
        
        info = [i,data[i]['file'].rstrip(".txt"),sentence]
        
        #L'element 0 est toujours la requete
        if i == 0:
            request = dict(zip(keys,info))
        else:
            result.append(dict(zip(keys,info)))
    
    return request,result





################################## FONCTIONS AUXILIAIRES ##################################
