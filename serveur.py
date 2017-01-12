from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys, json
from os import curdir, sep

#Solveur
import elementComparison


#Sous-classe d'un serveur http
class MyHandler(BaseHTTPRequestHandler):
    
    #Methode GET
    def do_GET(self):
        
        #Validation que la page est un html et qu'elle existe
        try :
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(f.read(),"utf-8"))
                f.close()
                return
            return
    
        #Erreur 404
        except IOError :
            self.send_error(404, 'Fichier indisponible : %s' % self.path)
            return

    #methode POST
    def do_POST(self):
        #LECTURE
        length = int(self.headers.get('content-length', 0))
        str_response = self.rfile.read(length).decode('utf-8')
        request = json.loads(str_response)

        requestText = elementComparison.readElement(request["cours"]+".txt")

        #REQUETE INVALIDE
        if requestText == -1:
            result = {"request":{"title":"requete invalide"},"result":[]}
            print("Requete Invalide: ",request["cours"])

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(bytes(json.dumps(result),"utf-8"))
            return -1


        #REQUETE VALIDE
        
        #Calcul du vecteur de mots
        query = elementComparison.getWordVector(requestText)
        
        #Calcul du coefficient de similitude
        result = elementComparison.getSimilitudeCoefficientsCosine(query)
        
        #Reorganisation en ordre decroissant de value et conservation de 10 elements. L'element 0 est la requete
        data = elementComparison.sortData(11,result,'value')
        
        #Mise en forme du resultat
        print("Requete: ",request["cours"])
        request,result = elementComparison.formatResponse(data)
        result = {"request":request,"result":result}

        #Envoi de la response au client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(json.dumps(result),"utf-8"))
        
        return 0

#Fonction principale
def main():
    
    #Initialisation du serveur
    try:
        print("Analyse de l'espace de mots... ",end="")
        elementComparison.getWordSpace()
        print("Fait")
        
        print("Calcul de la matrice tf... ",end="")
        elementComparison.getTfMatrix()
        print("Fait")
        
        print("Calcul du vecteur idf...",end="")
        elementComparison.getIdfVector()
        print("Fait")
        
        print("Demarrage du serveur... ",end="")
        server = HTTPServer(('',8081), MyHandler)
        print("Fait")
        
        server.serve_forever()

    #Interruption du serveur
    except KeyboardInterrupt:
        print("Arret du serveur...",end="")
        server.socket.close()
        print("Fait")


main()
