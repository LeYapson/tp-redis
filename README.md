# Introduction
Ce TP avait pour objectif de nous familiariser avec Redis, un système de gestion de base de données clé-valeur en mémoire, et de comprendre son utilisation dans un environnement distribué. Nous avons également intégré Redis dans une application web pour améliorer les performances en utilisant le cache.
## Partie 1 – Installation de Redis
1.	Installation de Redis :
o	Nous avons installé Redis sur notre machine en utilisant Docker. Cela nous a permis de lancer rapidement un conteneur Redis sans avoir à configurer manuellement l'environnement.
o	Commande utilisée :
o	Copier
```bash
docker run --name my-redis -d -p 6379:6379 redis
```
2.	Vérification du service :
o	Nous avons vérifié que le service Redis fonctionnait correctement en nous connectant au conteneur et en exécutant la commande ping.
o	Commande utilisée :
o	Copier
```bash
docker exec -it my-redis redis-cli ping
```
3.	Configuration pour les accès distants :
o	Nous avons configuré Redis pour permettre les accès distants en modifiant le fichier de configuration redis.conf et en redémarrant le service.
## Partie 2 – Architecture distribuée : réplication ou clustering
Nous avons choisi l'option de réplication Master/Slave pour ce TP.
1.	Configuration du Master et des Slaves :
o	Nous avons lancé un conteneur Redis master et un conteneur Redis slave en utilisant Docker.
o	Commandes utilisées :
o	Copier
```bash
docker run --name redis-master -d -p 6379:6379 redis
```
```bash
docker run --name redis-slave -d -p 6380:6379 redis redis-server --slaveof redis-master 6379
```
0.	Vérification de la réplication :
o	Nous avons vérifié que la réplication fonctionnait correctement en nous connectant au master et au slave et en exécutant la commande info replication.
o	Commandes utilisées :
o	Copier
```bash
docker exec -it redis-master redis-cli info replication
```
```bash
docker exec -it redis-slave redis-cli info replication
```
## Partie 3 – Intégration dans une application web
Nous avons créé une petite application web en Python utilisant Flask et Redis pour simuler une base de données lente et intégrer Redis en tant que cache.
1.	Installation des dépendances :
o	Nous avons installé les dépendances nécessaires en utilisant pip.
o	Commande utilisée :
o	Copier
```bash
pip install flask redis
```
2.	Code de l'application :
o	Nous avons écrit le code de l'application Flask qui utilise Redis comme cache. L'application vérifie d'abord si la donnée est dans Redis. Si elle est trouvée, elle est renvoyée immédiatement. Sinon, l'application simule une réponse lente, renvoie la réponse, et l'enregistre dans Redis avec une durée de vie courte.
o	Code utilisé :
o	Copier
```python
from flask import Flask, jsonify
import redis
import time

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/data/<key>')
def get_data(key):
    # Vérifie si la donnée est dans Redis
    cached_data = r.get(key)
    if cached_data:
        return jsonify({"data": cached_data.decode('utf-8'), "source": "cache"})

    # Simule une réponse lente
    time.sleep(2)
    data = f"value for {key}"
    # Stocke la donnée dans Redis avec une durée de vie de 60 secondes
    r.setex(key, 60, data)
    return jsonify({"data": data, "source": "database"})

if __name__ == '__main__':
•	    app.run(debug=True)
```
0.	Lancement de l'application :
o	Nous avons lancé l'application Flask en exécutant le fichier Python contenant notre code.
o	Commande utilisée :
o	Copier
```bash
python app.py
```
## Partie 4 – Vérification et démonstration
1.	Gain de performance :
o	Nous avons fait une requête à l'application pour une clé spécifique et noté le temps de réponse. Nous avons ensuite fait une seconde requête pour la même clé et noté que le temps de réponse était plus rapide, ce qui démontre le gain de performance grâce au cache.
2.	Donnée temporaire :
o	Nous avons attendu 60 secondes et fait une nouvelle requête pour la même clé. Nous avons noté que la réponse était à nouveau lente, ce qui démontre que la donnée était temporaire et avait expiré.
3.	Fonctionnement distribué :
o	Nous avons vérifié que la réplication des données entre le master et le slave fonctionnait correctement en consultwant les logs et en exécutant des commandes de vérification sur les conteneurs Redis.
# Conclusion
Ce TP nous a permis de comprendre l'utilisation de Redis dans un environnement distribué et son intégration dans une application web pour améliorer les performances. Nous avons appris à configurer Redis, à mettre en place une réplication Master/Slave, et à utiliser Redis comme cache dans une application web. Ces compétences seront utiles pour optimiser les performances des applications web et gérer des bases de données distribuées.

