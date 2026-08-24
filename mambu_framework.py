# Mambu Career Framework Descriptors
# Used for evaluating candidates against Mambu's internal leveling system

MAMBU_LEVELS = {
    8: {
        "title": "Intern/Engineer Entry",
        "ic_description": "Entry-level technical role. Learning fundamental concepts. Requires supervision and mentoring.",
        "tl_description": "N/A - Not applicable at this level"
    },
    7: {
        "title": "Associate",
        "ic_description": "Developing skills in assigned technical area. Beginning to work independently on defined tasks.",
        "tl_description": "N/A - Not applicable at this level"
    },
    6: {
        "title": "Intermediate",
        "ic_description": "Solid technical competency. Can work independently on most tasks. Growing expertise in professional area(s).",
        "tl_description": "N/A - Not applicable at this level"
    },
    5: {
        "title": "Experienced",
        "ic_description": "Strong technical expertise. Independently solves complex problems. Demonstrates mastery in discipline. May mentor juniors.",
        "tl_description": "N/A - Not applicable at this level"
    },
    4: {
        "title": "Senior",
        "ic_description": "Expert-level technical skills. Drives architecture decisions. Cross-functional impact. Mentors team members.",
        "tl_description": "Manager/Team Lead. Manages team, sets direction, deploys resources. Accountable for team performance. Results through others."
    },
    3: {
        "title": "Advanced Senior",
        "ic_description": "Deep domain expertise. Drives technical strategy. Significant impact across teams. Strong technical leadership.",
        "tl_description": "Senior Manager/3B. Extended span of management. Responsible for business performance. Strategic impact."
    },
    2: {
        "title": "Fellow (Tech/Product) / VP / SVP",
        "ic_description": "Distinguished expert role. Can only be initiated by LT. Recognition of breadth and impact.",
        "tl_description": "Director / Senior Director / VP / SVP. Strategic leadership. Manages multiple teams. Company-wide impact."
    },
    1: {
        "title": "LT (Leadership Team)",
        "ic_description": "N/A - Not applicable",
        "tl_description": "Leadership Team member. Executive role."
    },
    0: {
        "title": "CEO",
        "ic_description": "N/A - Not applicable",
        "tl_description": "Chief Executive Officer"
    }
}

MAMBU_KEY_PRINCIPLES = """
Key Principles of Job Levelling at Mambu:

1. 80/20 Rule: Mandatory skills are a must at assessed level. At least 80% of role requirements must be present.

2. Organizational Context: Consider where roles fit within team/function relative to each other.

3. Role Assessment: Assess the role (not the particular person). Disregard current title.

4. Career Path: Recognition of career trajectory - some roles only exist at lower levels and progress requires lateral change.

5. Job Scope: Refers to size and relative seniority/impact of the role within Mambu.

6. Disregard Current Pay: Focus on job and scope, not historical reasons for current pay.

7. Correct Understanding: Understanding what activities must the placeholder perform, how it impacts business.

8. 6-12 Month Evolution: Keeping in mind how the role might evolve over next 6-12 months.
"""

CAREER_PATHS = {
    "IC": {
        "name": "Individual Contributor",
        "description": "Work primarily achieved by individual or through project teams, with emphasis on technical/discipline knowledge rather than leading people."
    },
    "TL": {
        "name": "Team Leader",
        "description": "Accountable for leading people, setting direction and deploying resources; results primarily achieved through work of others."
    }
}

def get_level_descriptor(level: int, career_path: str = "IC") -> str:
    """Get descriptor for a specific Mambu level and career path"""
    if level not in MAMBU_LEVELS:
        return "Invalid level"

    level_info = MAMBU_LEVELS[level]

    if career_path == "TL":
        return level_info["tl_description"]
    else:
        return level_info["ic_description"]

def get_mambu_framework_prompt() -> str:
    """Get the Mambu framework as a formatted prompt for AI evaluation"""

    prompt = f"""
MAMBU CAREER FRAMEWORK - CONTEXT FOR EVALUATION

{MAMBU_KEY_PRINCIPLES}

LEVEL OVERVIEW:
Level 8 (Intern/Entry) → Entry-level learning
Level 7 (Associate) → Developing independence
Level 6 (Intermediate) → Solid competency
Level 5 (Experienced) → Expert-level skills
Level 4 (Senior) → Mastery, drives decisions
Level 3 (Advanced Senior) → Domain expert
Level 2 (Fellow/Director/VP) → Strategic role
Level 1 (LT) → Leadership team
Level 0 (CEO) → Executive

CAREER PATHS:
- IC (Individual Contributor): Technical leadership, deep expertise
- TL (Team Leader): People management, organizational leadership

IMPORTANT:
- 80/20 rule applies: At least 80% of role requirements must be present
- Assess the role, not the person's title
- Consider job scope (size and relative seniority)
"""
    return prompt
