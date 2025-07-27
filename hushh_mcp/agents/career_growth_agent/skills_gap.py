import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor

# Load the spaCy model
nlp = spacy.load("en_core_web_lg")

# Initialize the SkillExtractor with the EMSI skill database
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

def extract_job_skills_from_postings(descriptions: list[str]) -> set[str]:
    all_skills = set()

    for desc in descriptions:
        annotations = skill_extractor.annotate(desc)

        # Extract skills from both 'full_matches' and 'ngram_scored'
        for match in annotations['results'].get('full_matches', []):
            all_skills.add(match['doc_node_value'].lower())

        for match in annotations['results'].get('ngram_scored', []):
            all_skills.add(match['doc_node_value'].lower())

    return all_skills


def compute_skill_gaps(user_skills: set[str], job_skills: set[str]) -> set[str]:
    return {skill for skill in job_skills if skill not in user_skills}
