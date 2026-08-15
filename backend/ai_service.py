"""
Offline AI Service module for StudyTrack AI.
Provides deterministic note summarization, mock vector embedding, cosine similarity calculation,
and semantic search across study notes without any external API or network dependencies.
"""

import math
import re
from typing import List, Dict, Any

# Exact 12-word vocabulary specification in order
VOCABULARY = [
    "sort",
    "search",
    "binary",
    "insertion",
    "sql",
    "join",
    "fastapi",
    "pydantic",
    "prompt",
    "llm",
    "database",
    "validate"
]

# Exact 5 study notes specification
DEFAULT_NOTES = [
    {
        "note_id": 1,
        "text": "Binary search requires a sorted array and repeatedly halves the search range using a midpoint comparison."
    },
    {
        "note_id": 2,
        "text": "Insertion sort builds a sorted list one element at a time by shifting larger elements to the right."
    },
    {
        "note_id": 3,
        "text": "FastAPI uses Pydantic models to validate request bodies and automatically generates Swagger documentation."
    },
    {
        "note_id": 4,
        "text": "SQL joins combine rows from two tables using a matching column, such as inner join, left join, and full join."
    },
    {
        "note_id": 5,
        "text": "Prompt engineering structures a task, context, constraints, and desired output format to guide an LLM's response."
    }
]


def summarize_notes(raw_text: str) -> Dict[str, Any]:
    """
    Summarize notes using deterministic offline rules.
    
    Rules:
    - topic: First non-empty line (or "untitled" if empty)
    - key_points: First 3 non-empty sentences split on '.', '!', '?'
    - difficulty:
      - < 40 words -> "easy"
      - 40–100 words -> "medium"
      - > 100 words -> "hard"
    - Empty or whitespace input returns {"topic": "untitled", "key_points": [], "difficulty": "easy"}
    """
    if not raw_text or not raw_text.strip():
        return {
            "topic": "untitled",
            "key_points": [],
            "difficulty": "easy"
        }

    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    topic = lines[0] if lines else "untitled"

    # Split on sentence delimiters . ! ?
    raw_sentences = re.split(r'[.!?]+', raw_text)
    key_points = []
    for s in raw_sentences:
        cleaned = s.strip()
        if cleaned:
            key_points.append(cleaned)
            if len(key_points) == 3:
                break

    # Calculate total word count
    words = [w for w in re.split(r'\s+', raw_text.strip()) if w]
    word_count = len(words)

    if word_count < 40:
        difficulty = "easy"
    elif word_count <= 100:
        difficulty = "medium"
    else:
        difficulty = "hard"

    return {
        "topic": topic,
        "key_points": key_points,
        "difficulty": difficulty
    }


def mock_embed(text: str) -> List[float]:
    """
    Generate a 12-dimensional vector embedding for text based on VOCABULARY word counts.
    
    Rules:
    - Lowercase text
    - Split on runs of non-alphanumeric characters
    - Exact token matching (no stemming)
    - Returns list of 12 float frequency values
    """
    if not text:
        return [0.0] * len(VOCABULARY)

    # Tokenize: lowercase and split on non-alphanumeric characters
    tokens = [t for t in re.split(r'[^a-z0-9]+', text.lower()) if t]

    # Count occurrences of each vocabulary word
    token_counts = {}
    for token in tokens:
        token_counts[token] = token_counts.get(token, 0) + 1

    vector = [float(token_counts.get(word, 0)) for word in VOCABULARY]
    return vector


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculates Cosine Similarity from first principles:
    dot_product / (magnitude_A * magnitude_B)
    
    If either vector has magnitude 0, return 0.0 without divide-by-zero error.
    """
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    mag_a = math.sqrt(sum(a * a for a in vec1))
    mag_b = math.sqrt(sum(b * b for b in vec2))

    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot_product / (mag_a * mag_b)


def search_notes(query: str) -> List[Dict[str, Any]]:
    """
    Ranks the 5 default notes by descending cosine similarity score with query vector.
    For zero-vector queries (no vocabulary matches), preserves original note id order
    and returns 0.0 scores without failing.
    """
    query_vec = mock_embed(query)

    results = []
    for note in DEFAULT_NOTES:
        note_vec = mock_embed(note["text"])
        sim_score = cosine_similarity(query_vec, note_vec)
        results.append({
            "note_id": note["note_id"],
            "text": note["text"],
            "score": round(sim_score, 4)
        })

    # Sort by score descending; stable sort preserves original note_id order on tie (0.0 scores)
    ranked = sorted(results, key=lambda x: x["score"], reverse=True)
    return ranked
