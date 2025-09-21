Automated Resume Relevance Check System

Team Phoenix – Code4Tech Challenge | Generative AI Theme

Project Overview

This project automates resume evaluation for recruitment using a hybrid AI approach. It combines rule-based hard matching and LLM-powered semantic analysis to generate:

Relevance Score (0–100)

Fit Verdict: High / Medium / Low

Missing skills & personalized improvement suggestions

It saves recruiters time, ensures consistent evaluations, and provides actionable feedback to students.

Features

Upload Job Descriptions (JDs) and Resumes (PDF/DOCX)

Parsing & text extraction (PyMuPDF, docx2txt)

Hard Match: Skill & keyword checks (exact/fuzzy)

Semantic Match: Contextual similarity using embeddings & LLM (partial)

Output Generation: Score, verdict, missing skills, summary cards

Dashboard: Search, filter, shortlist candidates

Database: Stores results & logs (SQLite)

Completion Status
Feature / Component	Status	% Completion
Problem Statement	✅ Done	100%
Objective	✅ Done	100%
Sample Data	✅ Done	100%
Resume + JD Parsing	✅ Done (PyMuPDF, docx2txt)	100%
Hard Match Scoring	✅ Done	100%
Semantic Match Scoring	✅ Done (placeholder using embeddings)	80%
Weighted Score & Verdict	✅ Placeholder done	80%
Output Generation	✅ Done (cards, summary, missing skills)	100%
Database Storage	✅ Done (SQLite integrated)	100%
Dashboard / Filter / Search	✅ Done	100%
Frontend (Streamlit)	✅ Done	100%
LLM-based Feedback / Suggestions	⚠ Not implemented	0%

Overall: Core MVP functional (~95% complete); advanced AI feedback pending (~5% left).
Architecture
Frontend: Streamlit (upload, dashboard)
Backend: Flask / FastAPI
Engines:

Parsing & NLP preprocessing

Hard Matching Engine

Semantic Matching Engine (embeddings + LLM)

Scoring Engine

Database: SQLite
