from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.db_handeling.db.models import Role, RoleSkill, Skill, SkillAlias  # noqa: E402


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def _seed_roles(session: Session) -> tuple[dict[str, Role], int]:
    role_names = [
        "Backend Engineer",
        "Fullstack Developer",
        "Data Analyst",
        "Data Scientist",
        "ML Engineer",
        "DevOps Engineer",
    ]

    inserted = 0
    roles_by_normalized: dict[str, Role] = {}

    for role_name in role_names:
        normalized_name = normalize(role_name)
        role = session.execute(
            select(Role).where(Role.normalized_name == normalized_name)
        ).scalar_one_or_none()
        if role is None:
            role = Role(
                name=role_name,
                normalized_name=normalized_name,
            )
            session.add(role)
            session.flush()
            inserted += 1
        roles_by_normalized[normalized_name] = role

    return roles_by_normalized, inserted


def _seed_skills(session: Session) -> tuple[dict[str, Skill], int]:
    starter_skills: list[tuple[str, str]] = [
        ("Python", "Programming Languages"),
        ("JavaScript", "Programming Languages"),
        ("SQL", "Programming Languages"),
        ("TypeScript", "Programming Languages"),
        ("Bash", "Programming Languages"),
        ("Flask", "Backend"),
        ("FastAPI", "Backend"),
        ("REST", "Backend"),
        ("Authentication", "Backend"),
        ("JWT", "Backend"),
        ("SQLAlchemy", "Backend"),
        ("GraphQL", "Backend"),
        ("PostgreSQL", "Databases"),
        ("Redis", "Databases"),
        ("MySQL", "Databases"),
        ("MongoDB", "Databases"),
        ("Docker", "DevOps"),
        ("CI/CD", "DevOps"),
        ("Linux", "DevOps"),
        ("Git", "DevOps"),
        ("Kubernetes", "DevOps"),
        ("Terraform", "DevOps"),
        ("Monitoring", "DevOps"),
        ("NumPy", "ML Foundations"),
        ("Pandas", "ML Foundations"),
        ("scikit-learn", "ML Foundations"),
        ("Statistics", "ML Foundations"),
        ("Data Visualization", "ML Foundations"),
        ("Excel", "ML Foundations"),
        ("PyTorch", "Deep Learning"),
        ("TensorFlow", "Deep Learning"),
        ("Model Serving", "MLOps/Deployment"),
        ("APIs for ML", "MLOps/Deployment"),
        ("MLflow", "MLOps/Deployment"),
    ]

    inserted = 0
    skills_by_normalized: dict[str, Skill] = {}

    for skill_name, category in starter_skills:
        normalized_name = normalize(skill_name)
        skill = session.execute(
            select(Skill).where(Skill.normalized_name == normalized_name)
        ).scalar_one_or_none()
        if skill is None:
            skill = Skill(
                name=skill_name,
                normalized_name=normalized_name,
                category=category,
            )
            session.add(skill)
            session.flush()
            inserted += 1
        skills_by_normalized[normalized_name] = skill

    return skills_by_normalized, inserted


def _seed_skill_aliases(session: Session, skills_by_normalized: dict[str, Skill]) -> int:
    alias_map: list[tuple[str, str]] = [
        ("containerization", "Docker"),
        ("continuous integration", "CI/CD"),
        ("relational database", "PostgreSQL"),
        ("object relational mapper", "SQLAlchemy"),
        ("rest api", "REST"),
        ("auth", "Authentication"),
    ]

    inserted = 0

    for alias_text, canonical_skill_name in alias_map:
        normalized_alias = normalize(alias_text)
        normalized_skill_name = normalize(canonical_skill_name)
        skill = skills_by_normalized.get(normalized_skill_name)
        if skill is None:
            continue

        existing_alias = session.execute(
            select(SkillAlias).where(SkillAlias.normalized_alias == normalized_alias)
        ).scalar_one_or_none()
        if existing_alias is None:
            alias = SkillAlias(
                skill_id=skill.id,
                alias=alias_text,
                normalized_alias=normalized_alias,
            )
            session.add(alias)
            inserted += 1

    return inserted


def _seed_role_skill_mappings(
    session: Session,
    roles_by_normalized: dict[str, Role],
    skills_by_normalized: dict[str, Skill],
) -> int:
    mapping: dict[str, list[str]] = {
        "Backend Engineer": [
            "Python",
            "SQL",
            "PostgreSQL",
            "REST",
            "Authentication",
            "JWT",
            "Docker",
            "Git",
            "Linux",
        ],
        "Fullstack Developer": [
            "JavaScript",
            "Python",
            "REST",
            "PostgreSQL",
            "Git",
            "Docker",
        ],
        "Data Analyst": [
            "SQL",
            "Python",
            "Pandas",
            "Excel",
            "Data Visualization",
        ],
        "Data Scientist": [
            "Python",
            "Pandas",
            "NumPy",
            "scikit-learn",
            "Statistics",
            "SQL",
        ],
        "ML Engineer": [
            "Python",
            "scikit-learn",
            "PyTorch",
            "Docker",
            "Model Serving",
            "APIs for ML",
            "SQL",
        ],
        "DevOps Engineer": [
            "Docker",
            "CI/CD",
            "Linux",
            "Git",
            "PostgreSQL",
            "Monitoring",
        ],
    }

    inserted = 0

    for role_name, skill_names in mapping.items():
        role = roles_by_normalized.get(normalize(role_name))
        if role is None:
            continue

        for skill_name in skill_names:
            skill = skills_by_normalized.get(normalize(skill_name))
            if skill is None:
                continue

            existing_pair = session.execute(
                select(RoleSkill).where(
                    RoleSkill.role_id == role.id,
                    RoleSkill.skill_id == skill.id,
                )
            ).scalar_one_or_none()
            if existing_pair is None:
                role_skill = RoleSkill(
                    role_id=role.id,
                    skill_id=skill.id,
                )
                session.add(role_skill)
                inserted += 1

    return inserted


def main() -> int:
    load_dotenv(BACKEND_DIR / ".env")
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL is not set in backend/.env or environment.", file=sys.stderr)
        return 1

    engine = create_engine(
        database_url,
        future=True,
        pool_pre_ping=True,
    )
    session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        future=True,
    )

    inserted_summary = {
        "roles": 0,
        "skills": 0,
        "skill_aliases": 0,
        "role_skills": 0,
    }

    with session_local() as session:
        try:
            roles_by_normalized, inserted_summary["roles"] = _seed_roles(session)
            skills_by_normalized, inserted_summary["skills"] = _seed_skills(session)
            inserted_summary["skill_aliases"] = _seed_skill_aliases(
                session,
                skills_by_normalized,
            )
            inserted_summary["role_skills"] = _seed_role_skill_mappings(
                session,
                roles_by_normalized,
                skills_by_normalized,
            )

            session.commit()
        except Exception:
            session.rollback()
            raise

    print("Seed Summary")
    print(f"roles inserted: {inserted_summary['roles']}")
    print(f"skills inserted: {inserted_summary['skills']}")
    print(f"skill_aliases inserted: {inserted_summary['skill_aliases']}")
    print(f"role_skills inserted: {inserted_summary['role_skills']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
