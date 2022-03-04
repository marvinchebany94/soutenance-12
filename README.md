# soutenance-12

##PROJET 12

Pour ce projet il fallait créer une api dans laquelle des comptes appartenant soit à l'équipe de vente soit à l'équipe de gestion auront certains droits.

-----Compte vendeur-----
Un compte de l'équipe de vente pourra créer des clients, voir ses propres clients, modifier ses propres clients, créer des contrats, modifier ses contrats, voir ses contrats puis créer un événement qu'il associera à un compte de l'équipe de gestion.

-----Compte support-----
Voir ses événements, modifier ses événements puis voir ses clients.

-----Compte admin-----
Le compte admin se connecte dans l'url /admin, l'admin à accés à toutes les tables, peut créer des comptes utilisateurs, les associer à un groupe, et peut creer/modifier/voir/supprimer les éléments de chaque table.
Le compte admin est : admin@gmail.com , mot de passe : admin

###ACTIVER L ENVIRONNEMENT

-lancer l'invite de commandes

-se rendre dans le dossier telecharGé grâce à la commande cd "chemin du dossier"

-python -m venv env

-cd env/Scripts

-activate

-cd ..

-cd ..

-pip install -r requirements.txt
