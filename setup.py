# Import de setuptools, utilisé pour construire et installer des packages Python
from setuptools import setup, find_packages

# Configuration du package
setup(
    name="customer_analytics",          # Nom du package
    version="0.1.0",                    # Version initiale
    author="fadwa",                     # Nom de l’auteur
    author_email="fadwaelamraoui@gmail.com",  # E-mail de contact

    description="Package modulaire pour l'analyse des achats clients",  # Courte description

    packages=find_packages(),           # Recherche automatiquement tous les sous-packages

    # Dépendances nécessaires pour que le package fonctionne
    install_requires=[
        "numpy==2.3.2",
        "pandas==2.3.1",
        "python-dateutil==2.9.0.post0",
        "python-dotenv==1.1.1",
        "pytz==2025.2",
        "six==1.17.0",
        "tzdata==2025.2"
    ],

    python_requires=">=3.8",            # Version minimale de Python requise

    # Création d’une commande exécutable en ligne de commande
    entry_points={
        "console_scripts": [
            # Permet d'exécuter la fonction main() dans customer_analytics/main.py
            "customer_analytics=customer_analytics.main:main",
        ],
    },

    include_package_data=True,          # Inclure les fichiers déclarés dans MANIFEST.in s’il y en a

    # Classification du package pour PyPI
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
