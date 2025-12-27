Système RAG d’Analyse de Dialogues – Architecture White-Box
Description

Ce projet implémente un système de Retrieval-Augmented Generation (RAG) destiné à transformer des transcriptions brutes de centres d’appels en une base de connaissances interactive, vérifiable et explicable.

Contrairement aux solutions de type boîte noire, cette implémentation adopte une architecture White-Box, dans laquelle chaque étape du pipeline (nettoyage, segmentation, vectorisation, recherche SQL, génération) est explicitement définie, contrôlable et auditable.

Le système permet d’interroger des conversations réelles entre agents et clients afin d’extraire :

des procédures opérationnelles,

des réponses types,

des analyses de conformité et de performance.

Objectifs du Projet

L’assistant répond exclusivement à partir des faits présents dans les transcriptions, sans hallucination.

Exemples de questions prises en charge :

Analyse de l’accueil
Comment l’agent identifie-t-il l’appelant ?

Extraction de solutions
Quelle réponse est donnée pour un problème de facturation ?

Vérification de conformité
L’agent a-t-il suivi le script de clôture ?

Justification des réponses
Chaque réponse est accompagnée des segments exacts utilisés comme sources.

Technologies Utilisées
Backend et Base de Données
Technologie	Version	Rôle
Python	3.11+	Langage principal et logique métier
PostgreSQL	16+	Stockage relationnel et vectoriel
pgvector	0.7+	Recherche sémantique par similarité cosinus
SQLAlchemy	2.0+	ORM et requêtes SQL explicites
Intelligence Artificielle (Exécution Locale)
Composant	Modèle	Caractéristiques
Embeddings	all-MiniLM-L6-v2	384 dimensions, rapide et efficace
LLM	Llama 3.1 (8B)	Exécution locale via Ollama, forte fidélité aux instructions
Structure du Projet
ai-expert-bot/
│
├── data/                               # Corpus brut (.txt)
│   ├── call_001.txt                    # Transcription 1
│   ├── call_002.txt                    # Transcription 2
│   └── ...
│
├── backend/                            # Logique White-Box
│   ├── db.py                           # Connexion PostgreSQL
│   ├── setup_db.py                     # Initialisation des tables et pgvector
│   ├── embeddings.py                   # Modèle SentenceTransformers
│   ├── ingest_data.py                  # Nettoyage et indexation
│   ├── retrieval.py                    # Recherche sémantique en SQL pur
│   ├── generation.py                   # Prompting et Ollama
│   └── rag_backend.py                  # Orchestration du pipeline RAG
│
├── ui.py                               # Interface Streamlit avec Evidence Log
├── requirements.txt                    # Dépendances Python
└── README.md                           # Documentation

Installation et Flux de Travail
Étape 1 : Préparation de la Base de Données

Initialiser PostgreSQL avec le support vectoriel :

python -m backend.setup_db

Étape 2 : Ingestion et Nettoyage des Données

Le script :

lit les fichiers texte,

supprime les balises inutiles (h:, c:),

segmente les dialogues en unités cohérentes,

calcule les embeddings,

stocke les données dans PostgreSQL.

python -m backend.ingest_data

Étape 3 : Lancement de l’Interface Utilisateur
streamlit run ui.py

Architecture du Flux RAG

Entrée utilisateur
Question saisie via l’interface Streamlit.

Vectorisation
Transformation de la question en vecteur de 384 dimensions.

Recherche sémantique SQL
Exécution d’une requête explicite :

SELECT content
FROM documents
ORDER BY embedding <=> query_vector
LIMIT 5;


Augmentation du contexte
Fusion de la question et des segments récupérés dans un prompt contrôlé.

Génération de la réponse
Llama 3.1 génère une réponse basée uniquement sur les sources fournies.

Valeur Ajoutée de l’Approche

Transparence totale
Chaque étape du pipeline est visible et vérifiable.

Souveraineté des données
Toutes les données restent locales. Aucun service cloud n’est utilisé.

Réduction des hallucinations
Le système retourne « Je ne sais pas » si l’information est absente du corpus.

Evidence Log
Les sources exactes sont exposées à l’utilisateur pour validation humaine.

Cas d’Usage Cibles

Audit qualité des centres d’appels

Formation et coaching des agents

Extraction de procédures métier

Vérification réglementaire et conformité
