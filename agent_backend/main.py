import os
import sys
import subprocess
import tempfile
from enum import Enum
from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Définition des class Pydantic pour la validation des données

class severite(Enum):
    Faible = "Faible"
    Moyenne = "Moyenne"
    Critique = "Critique"


class WebhookPayload(BaseModel):
    """ Structure des données recues depuis le portail support utilisateur"""
    ticket_id: str = Field(..., description="Identifiant unique du ticket d'incident")
    user_report: str = Field(..., description="Description du problème rédigée par l'utilisateur")

class RapportBug(BaseModel):
    """Structure de l'analyse produite par l'Agent 1"""
    resume: str = Field(..., description="Résumé concis du bug identifié")
    severite: severite = Field(..., description="Niveau de gravité: Faible, Moyenne, Critique")
    zones_suspectes: List[str] = Field(..., description="Liste des fonctions, méthodes ou modules de la codebase à vérifier suspectés d'être la cause du bug")

class ReproductionTest(BaseModel):
    """Structure produite par l'Agent 2"""
    cause_racine: str = Field(..., description="Explication technique de la cause racine exacte du bug dans le code")
    test_pytest_code: str = Field(..., description="Code Python complet du fichier de test Pytest permettant de reproduire le bug")
    nom_fichier_test: str = Field(default="test_reproduction.py", description="Nom du fichier de test Pytest à créer")

class CodeCorrection(BaseModel):
    """Structure du correctif de code produit par l'Agent 3"""
    code_fix: str = Field(..., description="Extrait de code ou fonction specifique contenant uniquement la correction apportee")
    explications: str = Field(..., description="Explications claires des modifications apportées")
    succes: bool = Field(default=True, description="Indique si la génération a réussi")

class SecurityAudit(BaseModel):
    """Structure de l'audit produit par l'Agent 4"""
    conforme_securite: bool = Field(..., description="True si le code respecte les bonnes pratiques SecOps")
    remarques_securite: str = Field(..., description="Audit détaillé de sécurité du code corrigé")
    pr_title: str = Field(..., description="Titre professionnel suggéré pour la Pull Request GitHub")


app = FastAPI(
    title="Pipeline Automatisé Multi-Agents de Bug Fixing",
    description="API Production recevant les tickets du Portail Support et déclenchant la résolution autonome par nos agents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Multi-Agent Bug Fixing API",
        "documentation": "/docs"
    }
