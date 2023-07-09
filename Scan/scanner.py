import nmap
from tqdm import tqdm
from pyfiglet import Figlet
from termcolor import colored
import os
import subprocess

custom_font = Figlet(font='digital')
ascii_art = custom_font.renderText('RICKZ, HACKING')
colored_ascii = colored(ascii_art, 'red')
print(colored_ascii)


ip = input("Quelle est l'adresse IP à scanner ? ")
max_port = int(input("Port Max : "))

# Création de la commande pour exécuter le script avec ProxyChains
commande = ["proxychains", "python3"] + [os.path.abspath(__file__)]

# Vérification si ProxyChains est déjà utilisé
if "proxychains" not in subprocess.run(["ps", "ax"], capture_output=True, text=True).stdout:
    print("Veuillez exécuter le script avec ProxyChains en utilisant la commande suivante :")
    print(" ".join(commande))
    exit()

scanner = nmap.PortScanner()
open_ports = []

with tqdm(total=max_port) as pbar:
	for port in range(1, max_port):
		try:
		    pbar.update(1)
		    result = scanner.scan(ip, str(port))
		    if scanner[ip]['tcp'][port]['state'] == 'open':
		        service_name = scanner[ip]['tcp'][port]['name']
		        service_version = scanner[ip]['tcp'][port]['version']
		        open_ports.append((port, service_name, service_version))
		        print("Port ouvert : {}".format(port))
		except Exception as e:
		    pbar.set_description(f"Error scanning port {port}")
		    print("Une erreur s'est produite lors du scan du port {} : {}".format(port, str(e)))

print("\nScan terminé. Ports ouverts trouvés :")
for port in open_ports:
    print("Port : {}, Service : {}, Version : {}".format(port[0], port[1], port[2]))

# Création du dossier avec l'adresse IP
os.mkdir(ip)
# Chemin du dossier créé
dossier_ip = os.path.join(os.getcwd(), ip)
# Chemin du fichier à créer
chemin_fichier = os.path.join(dossier_ip, "resultscan.txt")

# Écriture de la liste open_ports dans le fichier
with open(chemin_fichier, "w") as fichier:
    for port in open_ports:
        fichier.write("Port : {}, Service : {}, Version : {}\n".format(port[0], port[1], port[2]))

print("Les résultats ont été enregistrés dans le fichier resultscan.txt.")

