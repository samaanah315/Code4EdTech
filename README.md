Automated Resume Relevance Check System

Team Phoenix – Code4Tech Challenge | Generative AI Theme

Project Overview

This project automates resume evaluation for recruitment using a hybrid AI approach. It combines rule-based matching and LLM-powered semantic analysis to generate a Relevance Score, identify missing skills, and provide a fit verdict for each candidate.

Key benefits:

Saves time for recruiters.

Ensures consistent evaluations across candidates.

Provides actionable feedback to students for improving resumes.

Scalable solution for handling thousands of resumes efficiently.

Features

Upload Job Descriptions (JD) and Resumes.

Parsing and text extraction from PDF/DOCX resumes.

Hard Matching: Keyword & skill checks (exact/fuzzy).

Semantic Matching: Contextual analysis using LLM embeddings.

Generates:

Relevance Score (0–100)

Fit Verdict: High / Medium / Low

Missing Skills & Certifications

Personalized improvement feedback

Centralized recruiter dashboard for search, filter, and shortlist.

Architecture

Frontend: Streamlit Web App
Backend: Flask / FastAPI
Core Engines:

Parsing & NLP preprocessing

Hard Matching Engine

Semantic Matching Engine (LLM + embeddings)

Scoring Engine

Database: PostgreSQL / SQLite
Vector Store: Chroma / Pinecone for embeddings

Flow:

Frontend (Streamlit) 
     ↓
Backend (Flask/FastAPI) 
     ↓
Parsing → Hard Match → Semantic Match → Scoring Engine
     ↓
Vector Store + Database
     ↓
Recruiter Dashboard

Tech Stack

Core AI Engine:

Python, SpaCy, NLTK

TF-IDF, BM25

Web Application:

Frontend: Streamlit

Backend: Flask / FastAPI

Database: PostgreSQL / SQLite
