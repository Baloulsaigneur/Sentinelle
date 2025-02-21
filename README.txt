

███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
                                                                



Ce projet est une API d’automatisation de tests de sécurité web qui exécute des
analyses avec Nmap, Nuclei et Nikto pour identifier les failles de sécurité d'un 
site web. Il fonctionne en mode Docker et utilise FastAPI comme backend.

---

### **1. Gérer les Conteneurs Docker**
#### **Démarrer, Arrêter et Nettoyer Docker**
```
docker-compose up -d         # Lancer les conteneurs en arrière-plan (mode détaché)
docker-compose down          # Arrêter et supprimer les conteneurs
docker-compose restart       # Redémarrer les conteneurs
docker-compose stop          # Arrêter sans supprimer les conteneurs
docker-compose pause         # Suspendre temporairement les conteneurs
docker-compose unpause       # Reprendre les conteneurs suspendus
```

#### **Reconstruction des Conteneurs**
Si vous avez modifié le code source et que vous voulez forcer la reconstruction :
```
docker-compose up --build    # Recréer les images avant de démarrer
docker-compose build         # Construire les images sans démarrer les conteneurs
```

#### **Lister les Conteneurs Actifs**
```
docker ps                    # Afficher les conteneurs en cours d'exécution
docker ps -a                 # Afficher tous les conteneurs (même arrêtés)
```

#### **Supprimer les Conteneurs et Images**
Si vous souhaitez tout effacer et repartir de zéro :
```
docker-compose down --volumes   # Supprime les conteneurs et les volumes
docker rmi $(docker images -q)  # Supprime toutes les images Docker
docker system prune -a          # Supprime les conteneurs, images, volumes non utilisés
```

---

### **2. Gérer et Analyser les Logs**
#### **Consulter les Logs des Conteneurs**
```
docker-compose logs                # Voir tous les logs des services
docker-compose logs -f              # Voir les logs en temps réel
docker-compose logs backend         # Voir les logs uniquement du backend
docker logs poc-sentinelle-2-backend-1  # Voir les logs du conteneur backend spécifique
docker logs -f poc-sentinelle-2-backend-1  # Suivre les logs en direct
```

#### **Effacer les Logs Docker**
```
truncate -s 0 $(docker inspect --format='{{.LogPath}}' poc-sentinelle-2-backend-1)  # Efface les logs d'un conteneur spécifique
docker system prune --volumes      # Nettoyer les volumes et logs inutilisés
```

---

### **3. Déboguer et Interagir avec les Conteneurs**
#### **Entrer dans un Conteneur**
Si vous souhaitez exécuter des commandes à l'intérieur d'un conteneur :
```
docker exec -it poc-sentinelle-2-backend-1 sh  # Ouvrir un shell dans le backend
docker exec -it poc-sentinelle-2-nmap_worker sh  # Ouvrir un shell dans le worker Nmap
```

#### **Lister les Processus en Exécution**
```
docker top poc-sentinelle-2-backend-1  # Voir les processus actifs dans un conteneur
```

#### **Afficher les Variables d'Environnement d'un Conteneur**
```
docker exec poc-sentinelle-2-backend-1 env
```

---

### **4. Tester les Requêtes API**
#### **Effectuer un Scan via l’API**
```
curl -X POST "http://localhost:8000/scan/" \
-H "Content-Type: application/json" \
-d '{"target": "https://www.exemple.fr/"}'
```

#### **Récupérer les Résultats d’un Scan**
```
curl -X GET "http://localhost:8000/results/<task_id>"
```

#### **Obtenir un Résumé des Résultats**
```
curl -X GET "http://localhost:8000/summary/<task_id>"
```

#### **Vérifier si l’API est en ligne**
```
curl -X GET "http://localhost:8000/"
```

---

### **5. Gérer les Images Docker**
#### **Lister les Images**
```
docker images                # Voir toutes les images Docker installées
docker images | grep poc-sentinelle-2  # Filtrer les images spécifiques à votre projet
```

#### **Supprimer une Image Spécifique**
```
docker rmi poc-sentinelle-2-backend
```

#### **Nettoyer Toutes les Images Docker**
```
docker rmi $(docker images -q)  # Supprime toutes les images non utilisées
```

---

### **6. Vérifier le Réseau Docker**
#### **Lister les Réseaux**
```
docker network ls
```

#### **Inspecter un Réseau**
```
docker network inspect poc-sentinelle-2_default
```

#### **Tester la Connectivité entre Conteneurs**
Dans le conteneur **backend**, exécutez :
```
ping poc-sentinelle-2-nmap_worker
```
Cela permet de voir si les services peuvent communiquer entre eux.

---

### **7. Résoudre des Problèmes**
#### **Voir les Dernières Erreurs Docker**
```
journalctl -u docker --no-pager | tail -n 50  # Voir les dernières erreurs Docker
```

#### **Redémarrer Docker**
```
sudo systemctl restart docker
```

#### **Voir l’Espace Utilisé par Docker**
```
docker system df
```

---

## **Résumé des Commandes Essentielles**
| **Action** | **Commande** |
| --- | --- |
| **Démarrer les conteneurs** | `docker-compose up -d` |
| **Arrêter les conteneurs** | `docker-compose down` |
| **Redémarrer les conteneurs** | `docker-compose restart` |
| **Stopper sans supprimer** | `docker-compose stop` |
| **Suspendre/Reprendre les conteneurs** | `docker-compose pause` / `docker-compose unpause` |
| **Recréer et démarrer les conteneurs** | `docker-compose up --build` |
| **Construire les images sans démarrer** | `docker-compose build` |
| **Lister les conteneurs actifs** | `docker ps` |
| **Lister tous les conteneurs (actifs et stoppés)** | `docker ps -a` |
| **Supprimer les conteneurs et volumes** | `docker-compose down --volumes` |
| **Supprimer toutes les images Docker** | `docker rmi $(docker images -q)` |
| **Nettoyer Docker (conteneurs, images, volumes inutilisés)** | `docker system prune -a` |
| **Voir tous les logs** | `docker-compose logs` |
| **Voir les logs en temps réel** | `docker-compose logs -f` |
| **Voir les logs du backend** | `docker-compose logs backend` |
| **Voir les logs d’un conteneur spécifique** | `docker logs poc-sentinelle-2-backend-1` |
| **Suivre les logs en direct d’un conteneur** | `docker logs -f poc-sentinelle-2-backend-1` |
| **Effacer les logs d’un conteneur** | `truncate -s 0 $(docker inspect --format='{{.LogPath}}' poc-sentinelle-2-backend-1)` |
| **Entrer dans un conteneur en ligne de commande** | `docker exec -it poc-sentinelle-2-backend-1 sh` |
| **Lister les processus en exécution dans un conteneur** | `docker top poc-sentinelle-2-backend-1` |
| **Afficher les variables d’environnement d’un conteneur** | `docker exec poc-sentinelle-2-backend-1 env` |
| **Tester la connexion entre conteneurs** | `ping poc-sentinelle-2-nmap_worker` (depuis backend) |
| **Lister les images Docker installées** | `docker images` |
| **Filtrer les images spécifiques au projet** | `docker images` |
| **Supprimer une image spécifique** | `docker rmi poc-sentinelle-2-backend` |
| **Vérifier l’espace utilisé par Docker** | `docker system df` |
| **Lister les réseaux Docker** | `docker network ls` |
| **Inspecter un réseau Docker** | `docker network inspect poc-sentinelle-2_default` |
| **Vérifier les erreurs récentes de Docker** | `journalctl -u docker --no-pager` |
| **Redémarrer Docker** | `sudo systemctl restart docker` |
| **Effectuer un scan via l’API** | `curl -X POST "http://localhost:8000/scan/" -H "Content-Type: application/json" -d '{"target": "https://www.oteria.fr/"}'` |
| **Récupérer les résultats d’un scan** | `curl -X GET "http://localhost:8000/results/<task_id>"` |
| **Obtenir un résumé des résultats** | `curl -X GET "http://localhost:8000/summary/<task_id>"` |
| **Vérifier si l’API est en ligne** | `curl -X GET "http://localhost:8000/"` |
| **Exécuter un scan Nmap manuellement** | `docker run --rm poc-sentinelle-2-nmap_worker -sV www.oteria.fr` |
| **Exécuter un scan Nuclei manuellement** | `docker run --rm poc-sentinelle-2-nuclei_worker -u https://www.oteria.fr` |
| **Exécuter un scan Nikto manuellement** | `docker run --rm poc-sentinelle-2-nikto_worker -host www.oteria.fr` |