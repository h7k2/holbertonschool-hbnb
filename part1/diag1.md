sequenceDiagram
    participant Client
    participant API as API (Présentation)
    participant Logic as Logique Métier
    participant DB as Base de Données (Persistance)

    Client ->> API: POST /users (données d'inscription)
    API ->> Logic: créerUtilisateur(données)
    Logic ->> Logic: validerDonnées()
    Logic ->> DB: sauvegarderUtilisateur(données)
    DB -->> Logic: confirmerSauvegarde()
    Logic -->> API: utilisateurCréé
    API -->> Client: 201 Created (détails utilisateur)

    alt Erreur de validation
        Logic -->> API: erreurValidation
        API -->> Client: 400 Bad Request
    end

    alt Erreur de base de données
        DB -->> Logic: erreurBD
        Logic -->> API: erreurPersistance
        API -->> Client: 500 Internal Server Error
    end
