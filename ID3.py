#Pour que le code fonctionne, importer le fichier "all_virg.csv"

from traitlets.config.application import default
from numpy.core.numerictypes import maximum_sctype
import numpy as np
import pandas as pd
import math
import numpy as np
data = pd.read_csv("all_virg.csv", delimiter=",")
X = data[[ 'year', 'price', 'mileage', 'tax', 'mpg', 'engineSize']].values



class Noeud : 
  nomVarPrinc = None
  listeVoitures = []
  listePrix = []
  listeCoefVar = []
  listeGainInfo = []
  listeNoeudFils = []
  cvNoeud = None
  indiceVardecoupage = None
  rangTree = None
  moyenneVar = 0
  
  def constrNoeud(self, listeVoiture) :
    for i in range(len(listeVoiture)):
      l = list(listeVoiture[i])
      self.listeVoitures.append(l)
      self.listePrix.append(l[1])

  def decontrNoeud(self):
    self.nomVarPrinc = ""
    self.listeVoitures = []
    self.listeCoefVar = []
    self.listeGainInfo = []
    self.listeNoeudFils = []
    self.listePrix= []
    self.cvNoeud = 0
    self.indiceVardecoupage = -1
    self.rangTree = 0
    self.moyennVar = 0

  def CV(self,nbrvar):
    listvar = []
    listDansNoeud = []
    for j in range(nbrvar):
      listvar = []
      for i in range(len(self.listeVoitures)):
        listvar.append(self.listeVoitures[i][j])

      meanvar = (sum(listvar)/len(listvar))
      st_var = sum((I-meanvar)**2 for I in listvar)/len(listvar)
      cvvar = st_var/meanvar
      self.listeCoefVar.append(cvvar)
      listDansNoeud = listDansNoeud + listvar

    meanNoeud = (sum(listDansNoeud))/(len(listDansNoeud))
    st_Noeud = sum((I-meanNoeud)**2 for I in listDansNoeud)/len(listDansNoeud)
    self.cvNoeud = st_Noeud/meanNoeud

  def gainInfoDeb(self):
    for i in range(len(self.listeCoefVar)):
      temp = self.cvNoeud - self.listeCoefVar[i]
      self.listeGainInfo.append(temp)
    #for i in range(len(self.listeGainInfo)):
     # print(self.listeGainInfo[i])

    
    max = -1
    position = -1
    for i in range(len(self.listeGainInfo)):
      if max < self.listeGainInfo[i] :
        max = self.listeGainInfo[i]
        position = i
    self.indiceVardecoupage = position    
    
  def gainInfoTree(self, nMere,n2):
    for i in range(len(self.listeCoefVar)):
      temp = nMere.cvNoeud - ((self.listeCoefVar[i]*len(self.listeVoitures)+n2.listeCoefVar[i]*len(n2.listeVoitures))/(len(self.listeVoitures)+len(n2.listeVoitures)))
      self.listeGainInfo.append(temp)   
    max = -1
    position = -1
    for i in range(len(self.listeGainInfo)):
      if max < self.listeGainInfo[i] :
        max = self.listeGainInfo[i]
        position = i
    self.indiceVardecoupage = position    
      
 


class Tree():
  NoeudMere = None
  nbrdecoupage = 2
  listeNomVariable = ["year", "price", "mileage", "tax", "mpg", "engineSize"]
  listeTree = []

  def decoupage(self,posiVar,voituresDansNoeud, rang,listePrix ,noeud):
    varDecoup = []
    for i in range(len(voituresDansNoeud)):
      varDecoup.append(voituresDansNoeud[i][posiVar])
    moyenne = 0
    for i in range(len(varDecoup)):
      moyenne = moyenne + varDecoup[i]
    moyenne = moyenne/len(varDecoup)
    noeud.moyenneVar = moyenne
    noeud1 = Noeud()
    noeud1.decontrNoeud()
    noeud2 = Noeud()
    noeud2.decontrNoeud()

    noeud1.nomVarPrinc= self.listeNomVariable[posiVar]
    noeud2.nomVarPrinc= self.listeNomVariable[posiVar]
    


    for i in range(len(voituresDansNoeud)):
      if voituresDansNoeud[i][posiVar] < moyenne :
        voituresDansNoeud[i].pop(posiVar)
        noeud1.listeVoitures.append(voituresDansNoeud[i])
        noeud1.listePrix.append(listePrix[i])
      elif voituresDansNoeud[i][posiVar] > moyenne : 
        voituresDansNoeud[i].pop(posiVar)
        noeud2.listeVoitures.append(voituresDansNoeud[i])
        noeud2.listePrix.append(listePrix[i])

    
    noeud1.rangTree = rang
    noeud2.rangTree = rang
    

    self.listeTree.append(noeud1)
    self.listeTree.append(noeud2)
   

  def constructTree(self):
    n = Noeud()
    n.constrNoeud(X[0:88060])
    n.CV(len(self.listeNomVariable))
    n.gainInfoDeb()
    n.nomVarPrinc = "Noeud mere"
    self.NoeudMere = n 
    self.listeTree.append(n) 
    self.decoupage(self.NoeudMere.indiceVardecoupage, self.NoeudMere.listeVoitures,1, self.NoeudMere.listePrix, self.NoeudMere)
    self.listeNomVariable.pop(self.NoeudMere.indiceVardecoupage)
    a=1
    b=0
    c=2
    taille=4
    while len(self.listeNomVariable)>1:
          
      ntemp = self.listeTree[a]
      nmere = self.listeTree[b]
      nfrere = self.listeTree[c]
      nfrere.CV(taille)
      ntemp.CV(taille)
      ntemp.gainInfoTree(nmere,nfrere)
      #print("----------------------------------------")
      #verifier si il n'y a pas d'erreur, tester la majorité du rang de l'arbre peut être en fonction d'intervales dans la liste Tree calculer la majorité et comparé
      self.decoupage(ntemp.indiceVardecoupage, ntemp.listeVoitures,a+1,ntemp.listePrix,ntemp)
      if len(self.listeTree) == 7 or len(self.listeTree) == 15 or len(self.listeTree) == 31 or len(self.listeTree) == 63 : 
        self.listeNomVariable.pop(ntemp.indiceVardecoupage)
        taille = taille-1
        #for i in range(len(self.listeNomVariable)):
         # print(self.listeNomVariable[i])
      if (a%2) == 0 :
        c = a+1
        b = b+1
      else :
        c = a-1
      a =a+1
      #print(len(self.listeTree))
      
  

   


t = Tree()
t.constructTree()
#-------------------------------------------------------------------------------
#for i in range(len(t.listeTree)):
#  print(i)
#  print(t.listeTree[i].moyenneVar)
#  print(len(t.listeTree[i].listePrix))
listeNewVar = []
year = input("year?")
listeNewVar.append(int(year))
price = input("price?")
listeNewVar.append(int(price))
milage = input("milage?")
listeNewVar.append(int(milage))
tax = input("Tax?")
listeNewVar.append(int(tax))
mgp = input("mgp?")
listeNewVar.append(float(mgp))
engineSize = input("engineSize?")
listeNewVar.append(float(engineSize))

listeNomNew = [ "year", "price", "mileage", "tax", "mpg", "engineSize"]

listeVariable = []
a = 0
nom = ""


for i in range(5):
  indice = -1
  ntemp = t.listeTree[a]
  nom = t.listeTree[a*2+1].nomVarPrinc
  moyenne = t.listeTree[a].moyenneVar
  for j in range(len(listeNomNew)):
    if nom == listeNomNew[j]:
      indice = j
  if listeNewVar[indice]<moyenne : 
    a = a*2+1
  else :
    a = a*2+2

 

prix = 0
for i in range(len(t.listeTree[a].listePrix)):
  prix = prix + t.listeTree[a].listePrix[i]
prix = prix/len(t.listeTree[a].listePrix)

print("prix prédit : " + str(prix))


