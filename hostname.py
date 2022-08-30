import json
import instantpy
import csv
import time



print("!!!!!!!!!!!!!!!!!!!!!Salut, Vous voulez renommer les aps gérer par un VC????!!!!!!!!!!!!!")
print("Crée un fichier juste à cote avec le nom ap.csv avec 2 colonnes séparait avec une virgule : (hostname, Ip). ")
print ("dans ce qui suit on va vous demander l'ip, username et password du VC!!!!!!!!!!!!!!!!!!!!!!!")
device = input ("Entrer IP address VC:")
username = input ("Entrer username :")
password = input ("Entrer password :")
vc = instantpy.InstantVC(username, password, device)

with open('ap.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        host= row[0]
        ip= row[1]
        result = vc.hostname(name=host, iap_ip=ip)
        line_count += 1
    print(f'Processed {line_count} APs.')
print(json.dumps(result, indent=4))
time.sleep(5)
vc.logout()