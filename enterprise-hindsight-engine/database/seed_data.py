#!/usr/bin/env python3
"""
Synthetic Enterprise Data Generator
Populates the database with realistic enterprise accounts, contacts, deals, transcripts, and product feedback.
"""

import os
import sys
import random
import psycopg2
from datetime import datetime, timedelta
from decimal import Decimal

# Database connection parameters
DB_PARAMS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "hindsight"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}

# Sample data
COMPANIES = [
    ("Acme Corp", 500000, "Technology", "Enterprise"),
    ("Globex Industries", 750000, "Manufacturing", "Strategic"),
    ("Initech", 300000, "Software", "Enterprise"),
    ("Umbrella Corp", 1200000, "Biotech", "Strategic"),
    ("Wayne Enterprises", 2000000, "Conglomerate", "Strategic"),
    ("Stark Industries", 1800000, "Defense", "Strategic"),
    ("Oscorp", 900000, "Chemicals", "Enterprise"),
    ("Cyberdyne Systems", 600000, "AI/ML", "Growth"),
    ("Massive Dynamic", 1100000, "Research", "Strategic"),
    ("Weyland-Yutani", 1500000, "Space", "Enterprise"),
]

PERSONAS = ["CTO", "CFO", "CISO", "VP Engineering", "Procurement", "Champion", "Legal", "VP Sales"]

DEAL_STAGES = ["Discovery", "Technical Validation", "Negotiation", "Closed Won", "Closed Lost"]

CALL_STAGES = ["Discovery", "Technical Deep-Dive", "Negotiation", "Procurement Review", "Executive Alignment"]

OBJECTIONS_POOL = [
    "Pricing is above budget",
    "API latency concerns",
    "Security compliance (SOC2 Type II)",
    "Vendor lock-in risk",
    "Integration complexity with legacy stack",
    "Data residency requirements",
    "Competitor has feature X",
    "Implementation timeline too long",
    "No dedicated CSM assigned",
    "Contract terms too rigid",
    "ROI unclear for CFO",
    "Procurement requires 3 quotes",
]

FEEDBACK_CATEGORIES = ["Performance", "Security", "Integrations", "UI/UX", "Analytics", "API"]

FEEDBACK_SAMPLES = [
    ("Edge Caching", "Performance", "Need edge caching for APAC latency reduction"),
    ("SOC2 Type II", "Security", "Customer requires SOC2 Type II certification"),
    ("Salesforce Sync", "Integrations", "Bidirectional Salesforce sync is critical"),
    ("Dark Mode", "UI/UX", "Enterprise users demand full dark mode support"),
    ("Custom Dashboards", "Analytics", "Need drag-and-drop custom dashboard builder"),
    ("Webhook Retry", "API", "Webhook delivery needs exponential backoff retry"),
    ("SSO/SAML", "Security", "Enterprise SSO with SAML 2.0 required"),
    ("Bulk Export", "Analytics", "CSV/Parquet bulk export for data lake ingestion"),
    ("Mobile App", "UI/UX", "Native mobile app for field sales team"),
    ("GraphQL API", "API", "GraphQL endpoint for flexible data fetching"),
]


def get_connection():
    """Create database connection."""
    return psycopg2.connect(**DB_PARAMS)


def seed_accounts(cur):
    """Seed accounts table."""
    print("Seeding accounts...")
    account_ids = []
    for company_name, arr, industry, tier in COMPANIES:
        health_score = random.randint(60, 100)
        cur.execute(
            """
            INSERT INTO accounts (company_name, arr_value, health_score, industry, tier)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING account_id
            """,
            (company_name, arr, health_score, industry, tier),
        )
        account_ids.append(cur.fetchone()[0])
    return account_ids


def seed_contacts(cur, account_ids):
    """Seed contacts table."""
    print("Seeding contacts...")
    for account_id in account_ids:
        num_contacts = random.randint(3, 6)
        selected_personas = random.sample(PERSONAS, min(num_contacts, len(PERSONAS)))
        for i, persona in enumerate(selected_personas):
            name = f"{persona} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])}"
            email = f"{persona.lower()}.{account_id}.{i}@{COMPANIES[account_id % len(COMPANIES)][0].lower().replace(' ', '')}.com"
            cur.execute(
                """
                INSERT INTO contacts (account_id, name, persona, email, title)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (account_id, name, persona, email, persona),
            )


def seed_deals(cur, account_ids):
    """Seed deals table."""
    print("Seeding deals...")
    deal_ids = []
    for account_id in account_ids:
        num_deals = random.randint(1, 3)
        for _ in range(num_deals):
            stage = random.choice(DEAL_STAGES)
            arr_amount = Decimal(random.randint(100000, 2000000))
            owner = random.choice(["Sarah Chen", "Marcus Johnson", "Priya Patel", "James Wilson", "Lisa Park"])
            close_date = datetime.now() + timedelta(days=random.randint(30, 180))
            cur.execute(
                """
                INSERT INTO deals (account_id, deal_name, stage, arr_amount, owner, close_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING deal_id
                """,
                (account_id, f"Deal-{account_id}-{random.randint(1000, 9999)}", stage, arr_amount, owner, close_date.date()),
            )
            deal_ids.append(cur.fetchone()[0])
    return deal_ids


def seed_transcripts(cur, account_ids, deal_ids):
    """Seed call_transcripts table."""
    print("Seeding call transcripts...")
    for account_id in account_ids:
        account_deals = [d for d in deal_ids if random.random() < 0.3]
        num_calls = random.randint(5, 15)
        for i in range(num_calls):
            call_stage = random.choice(CALL_STAGES)
            num_objections = random.randint(0, 3)
            objections = random.sample(OBJECTIONS_POOL, num_objections) if num_objections > 0 else []
            sentiment = round(random.uniform(-0.5, 0.8), 2)
            days_ago = random.randint(0, 90)
            created_at = datetime.now() - timedelta(days=days_ago)
            deal_id = random.choice(account_deals) if account_deals else None

            transcript_text = f"""
Call {i+1} - {call_stage} with Account {account_id}
Duration: {random.randint(30, 60)} minutes
Attendees: {', '.join(random.sample(PERSONAS, random.randint(2, 4)))}
Key Discussion Points:
- Product fit for {COMPANIES[account_id % len(COMPANIES)][0]} use case
- Technical requirements review
- Timeline and implementation approach
- Pricing and contract terms discussion
Objections raised: {', '.join(objections) if objections else 'None'}
Next steps: {random.choice(['Technical deep-dive scheduled', 'POC timeline agreed', 'Security review initiated', 'Executive alignment meeting set'])}
            """.strip()

            cur.execute(
                """
                INSERT INTO call_transcripts (account_id, deal_id, call_stage, transcript_text, objections_raised, sentiment_score, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (account_id, deal_id, call_stage, transcript_text, objections, sentiment, created_at),
            )


def seed_feedback(cur, account_ids):
    """Seed product_feedback table."""
    print("Seeding product feedback...")
    for account_id in account_ids:
        num_feedback = random.randint(2, 5)
        selected_feedback = random.sample(FEEDBACK_SAMPLES, min(num_feedback, len(FEEDBACK_SAMPLES)))
        for feature, category, text in selected_feedback:
            arr_impact = Decimal(random.randint(50000, 500000))
            status = random.choice(["Open", "In Backlog", "In Progress", "Resolved"])
            cur.execute(
                """
                INSERT INTO product_feedback (account_id, feature_name, category, arr_weighted_impact, feedback_text, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (account_id, feature, category, arr_impact, text, status),
            )


def main():
    """Main seeding function."""
    print("=" * 60)
    print("Enterprise Deal & Revenue Intelligence Platform - Data Seeding")
    print("=" * 60)

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Seed in order due to foreign key constraints
        account_ids = seed_accounts(cur)
        conn.commit()
        print(f"Created {len(account_ids)} accounts")

        seed_contacts(cur, account_ids)
        conn.commit()
        print(f"Created contacts for all accounts")

        deal_ids = seed_deals(cur, account_ids)
        conn.commit()
        print(f"Created {len(deal_ids)} deals")

        seed_transcripts(cur, account_ids, deal_ids)
        conn.commit()
        print(f"Created call transcripts")

        seed_feedback(cur, account_ids)
        conn.commit()
        print(f"Created product feedback entries")

        cur.close()
        conn.close()

        print("=" * 60)
        print("✅ Seeding complete!")
        print("=" * 60)

    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\nMake sure PostgreSQL is running and environment variables are set:")
        print("  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()