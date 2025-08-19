# dashboard/ai_agent.py
from collections import Counter, defaultdict

def _normalize(skill: str) -> str:
    s = skill.strip().lower()
    # lightweight aliases / normalizations
    aliases = {
        "js": "javascript",
        "ts": "typescript",
        "py": "python",
        "c sharp": "c#",
        "cpp": "c++",
        "postgres": "postgresql",
        "ms sql": "sql",
        "mssql": "sql",
        "html5": "html",
        "css3": "css",
        "powerapps": "power apps",
        "powerautomate": "power automate",
        "azure devops": "devops",
    }
    return aliases.get(s, s)

def categorize_skills(skills: list[str]) -> dict[str, list[tuple[str, int]]]:
    """
    Categorize skills into buckets using a simple, free, rule-based approach.
    Returns:
      {
        "Languages": [("python", 3), ("java", 1)],
        "Frameworks": [("django", 2)],
        ...
      }
    """
    # 1) normalize + count
    norm_skills = [_normalize(s) for s in skills if s and s.strip()]
    counts = Counter(norm_skills)

    # 2) category keyword rules (expand anytime)
    rules = {
        "Languages": [
            "python", "java", "c", "c++", "c#", "go", "rust", "kotlin",
            "swift", "javascript", "typescript", "html", "css", "sql"
        ],
        "Frameworks": [
            "django", "flask", "fastapi", "spring", "react", "angular",
            "vue", "next", "nuxt", "express", "laravel", "rails", "selenium"
        ],
        "Databases": [
            "mysql", "postgresql", "sqlite", "mongodb", "mariadb", "redis",
            "dynamodb", "cosmosdb"
        ],
        "Cloud": [
            "aws", "azure", "gcp", "google cloud", "cloud run", "cloud functions",
            "lambda", "ec2", "s3", "azure devops"
        ],
        "DevOps": [
            "docker", "kubernetes", "helm", "terraform", "ansible", "github actions",
            "jenkins", "devops", "gitlab ci"
        ],
        "Tools": [
            "git", "postman", "power automate", "power apps", "jira", "notion",
            "vscode", "intellij", "pycharm"
        ],
        "Soft Skills": [
            "communication", "leadership", "teamwork", "problem solving",
            "time management", "presentation"
        ],
    }

    # 3) assign skills to categories by substring match
    categorized = defaultdict(list)
    for skill, cnt in counts.items():
        placed = False
        for cat, keywords in rules.items():
            # match if any keyword is a substring of the skill or vice-versa
            if any(kw in skill or skill in kw for kw in keywords):
                categorized[cat].append((skill, cnt))
                placed = True
                break
        if not placed:
            categorized["Other"].append((skill, cnt))

    # sort each list (most frequent first, then alpha)
    for cat in list(categorized.keys()):
        categorized[cat].sort(key=lambda x: (-x[1], x[0]))

    return dict(categorized)
