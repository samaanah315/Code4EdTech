# ---------- Example Inputs ----------
# Hard match results from your previous step
hard_match_results = {
    "must_have_pct": 66.66,  # % of must-have skills matched
    "good_to_have_pct": 66.66  # % of good-to-have skills matched
}

# Semantic match results from your previous step
semantic_match_results = {
    "Python": 0.33,
    "Git": 0.39,
    "SQL": 0.19,
    "Django": 0.30,
    "REST APIs": 0.39,
    "Docker": 0.36
}

# ---------- Weighted Scoring ----------
def compute_relevance_score(hard_match, semantic_match, weights=None):
    """
    Compute overall relevance score combining hard and semantic matches.
    
    weights: dictionary with weights for each component, e.g.
        {"must_have": 0.4, "good_to_have": 0.2, "semantic": 0.4}
    """
    if weights is None:
        weights = {"must_have": 0.4, "good_to_have": 0.2, "semantic": 0.4}
    
    # Hard match component
    hard_score = (
        hard_match["must_have_pct"] * weights["must_have"] +
        hard_match["good_to_have_pct"] * weights["good_to_have"]
    )
    
    # Semantic match component: average of all semantic skill scores (0-1 scaled to 0-100)
    semantic_score = sum(semantic_match.values()) / len(semantic_match) * 100
    semantic_score *= weights["semantic"]
    
    # Total weighted score
    total_score = hard_score + semantic_score
    return round(total_score, 2)

# ---------- Verdict ----------
def assign_verdict(score):
    if score >= 75:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"

# ---------- Run ----------
final_score = compute_relevance_score(hard_match_results, semantic_match_results)
verdict = assign_verdict(final_score)

print(f"Final Relevance Score: {final_score}")
print(f"Verdict: {verdict}")
