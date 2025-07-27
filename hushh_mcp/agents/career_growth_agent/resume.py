# hushh_mcp/agents/career_growth_agent/resume_parser.py

import fitz  # PyMuPDF
import re
from typing import List
from fastapi import HTTPException

# SkillNer Imports
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor

# Load spacy model once
nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

def extract_skills(text: str) -> List[str]:
    annotations = skill_extractor.annotate(text)
    full_matches = annotations.get("results", {}).get("full_matches", [])
    return list(set([match["doc_node_value"].lower() for match in full_matches]))

def parse_resume(file_bytes: bytes) -> dict:
    try:
        # Load PDF from bytes
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        # Normalize text
        text = text.lower()

        # === Skills Extraction using SkillNer ===
        found_skills = extract_skills(text)

        # === Experience Extraction ===
        exp_matches = re.findall(r"(?:intern|developer|engineer|researcher|analyst|consultant).{0,50}", text)
        experience = list(set(exp_matches))[:10]  # limit to top 10

        # === Education Extraction ===
        edu_matches = re.findall(r"(?:b\.tech|bachelor|master|ph\.?d|iit|nit|university|college).{0,80}", text)
        education = list(set(edu_matches))[:5]

        return {
            "skills": found_skills,
            "experience": experience,
            "education": education
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")
