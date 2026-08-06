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
from langchain.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

load_dotenv()

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
