Système RAG d'Analyse de Dialogues : "White-Box" Architecture📝 DescriptionImplémentation d'un système de Retrieval-Augmented Generation (RAG) conçu pour transformer des transcriptions brutes de centres d'appels en une base de connaissances interactive.Contrairement aux solutions "boîte noire", ce projet privilégie une architecture transparente où chaque étape (nettoyage, vectorisation, recherche SQL) est explicitement définie. Le système permet d'interroger des conversations réelles entre agents et clients pour extraire des procédures, des réponses types et des analyses de performance.🎯 Objectifs du ProjetL'objectif est de fournir un assistant capable de répondre avec précision en se basant uniquement sur les faits présents dans les transcriptions :📞 Analyse de l'accueil : "Comment l'agent identifie-t-il l'appelant ?"💡 Extraction de solutions : "Quelle réponse est donnée pour un problème de facturation ?"🔍 Vérification de conformité : "L'agent a-t-il suivi le script de clôture ?"📊 Preuve par l'image : Chaque réponse est accompagnée de ses sources exactes.🛠️ Technologies UtiliséesBackend & Base de DonnéesTechnologieVersionRôlePython3.11+Langage et logique métierPostgreSQL16+Stockage relationnel et vectorielpgvector0.7+Recherche sémantique par similarité cosinusSQLAlchemy2.0+Gestion transparente des requêtes SQLIntelligence Artificielle (100% Locale)ComposantModèleCaractéristiquesEmbeddingsall-MiniLM-L6-v2384 dimensions, optimisé pour la vitesseLLMLlama 3.1 (8B)Local via Ollama, haute fidélité aux instructions📁 Structure du ProjetPlaintextai-expert-bot/
│
├── 📂 data/                              ← CORPUS BRUT (.txt)
│   ├── call_001.txt                      Transcription 1
│   ├── call_002.txt                      Transcription 2
│   └── ...                               (Fichiers de dialogues)
│
├── 📂 backend/                           ← LOGIQUE "WHITE-BOX"
│   ├── db.py                             Connexion PostgreSQL
│   ├── setup_db.py                       Initialisation des tables & pgvector
│   ├── embeddings.py                     Modèle SentenceTransformers
│   ├── ingest_data.py                    Nettoyage & Indexation des fichiers
│   ├── retrieval.py                      Recherche sémantique (SQL pur)
│   ├── generation.py                     Logique de prompt & Ollama
│   └── rag_backend.py                    Orchestration du flux complet
│
├── 💻 ui.py                              ← INTERFACE UTILISATEUR
│    └── Interface Streamlit avec "Evidence Log"
│
├── 📦 requirements.txt                   ← Dépendances Python
└── 📖 README.md                          ← Documentation
🚀 Installation & Flux de TravailÉtape 1 : Préparation de la BaseExécuter le script de création de table pour préparer PostgreSQL à recevoir des vecteurs.Bashpython -m backend.setup_db
Étape 2 : Ingestion & Nettoyage (Flux Ingestion)Le script ingest_data.py lit les fichiers, supprime les tags inutiles (h:, c:), découpe le texte en segments (chunks) et les stocke.Bashpython -m backend.ingest_data
Étape 3 : Lancement de l'AssistantBashstreamlit run ui.py
🔧 Architecture du Flux CompletEntrée : L'utilisateur pose une question via Streamlit.Vectorisation : La question est transformée en vecteur (384D).Retrieval SQL : Une requête SQL cherche les segments les plus proches :SELECT content FROM documents ORDER BY embedding <=> query_vector LIMIT 5;Augmentation : La question et les segments trouvés sont fusionnés dans un prompt strict.Génération : Llama 3.1 génère une réponse sourcée.🌟 Valeur Ajoutée de l'Approche✅ Transparence Totale : Pas de fonctions cachées ; le passage du document à la base de données est auditable.✅ Souveraineté des Données : Aucune donnée ne quitte votre machine. Idéal pour la confidentialité des appels.✅ Fidélité (Anti-Hallucination) : Le système est configuré pour dire "Je ne sais pas" si l'information est absente des transcriptions.✅ Evidence Log : L'interface affiche les segments originaux pour que l'utilisateur puisse vérifier l'IA.
