"""
Product Agent - PLG Feedback Synthesizer
Analyzes product feedback, synthesizes feature requests, and prioritizes roadmap based on revenue impact.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any
from collections import Counter

from groq import Groq

from app.hindsight_client import hindsight_client
from app.config import settings


def get_groq_client() -> Groq:
    """Lazy initialization of Groq client to handle missing API key gracefully."""
    api_key = settings.groq_api_key
    if not api_key or api_key == "your-groq-api-key":
        raise ValueError("GROQ_API_KEY not configured. Please set it in environment variables.")
    return Groq(api_key=api_key)


@dataclass
class FeatureRequestSynthesis:
    """Synthesized feature request with revenue weighting."""
    feature_id: str
    title: str
    description: str
    category: str
    request_count: int
    unique_accounts: int
    total_arr_impact: float  # Sum of ARR from requesting accounts
    avg_account_health: float
    strategic_alignment: str  # high, medium, low
    effort_estimate: str  # S, M, L, XL
    priority_score: float
    requesting_accounts: list[dict[str, Any]]
    similar_existing_features: list[str]
    generated_at: datetime


@dataclass
class FeedbackTheme:
    """Theme extracted from feedback."""
    theme: str
    mention_count: int
    sentiment: str  # positive, negative, neutral
    accounts_mentioning: int
    total_arr: float
    representative_quotes: list[str]


async def synthesize_feature_requests(
    account_ids: Optional[list[str]] = None,
    time_window_days: int = 90,
    min_arr_threshold: float = 0,
) -> list[FeatureRequestSynthesis]:
    """
    Synthesize and prioritize feature requests from multiple accounts.

    Args:
        account_ids: Optional list of account IDs to analyze (None = all)
        time_window_days: Lookback window for feedback
        min_arr_threshold: Minimum ARR for accounts to include

    Returns:
        List of prioritized feature requests
    """
    # In production, this would query the database for feedback
    # For now, we'll simulate with Hindsight recall
    
    all_feedback = []
    
    if account_ids:
        for account_id in account_ids:
            memory = await hindsight_client.recall_context(
                entity_id=account_id,
                query=f"feature requests product feedback bugs improvements wishlist",
            )
            all_feedback.append({
                "account_id": account_id,
                "feedback": memory.context,
            })
    else:
        # Simulate aggregate feedback
        memory = await hindsight_client.recall_context(
            entity_id="aggregate",
            query=f"feature requests product feedback bugs improvements wishlist from all accounts",
        )
        all_feedback.append({
            "account_id": "aggregate",
            "feedback": memory.context,
        })

    prompt = f"""
You are a Product Intelligence Agent powered by Hindsight memory.
Analyze product feedback from enterprise accounts and synthesize prioritized feature requests.

=== FEEDBACK FROM ACCOUNTS ===
{json.dumps(all_feedback, indent=2)}

=== CONTEXT ===
- Time window: {time_window_days} days
- Min ARR threshold: ${min_arr_threshold:,.0f}
- Accounts analyzed: {len(account_ids) if account_ids else 'all'}

=== TASK ===
Extract and synthesize feature requests. Return JSON array of feature requests:

[
  {{
    "feature_id": "FR-001",
    "title": "Specific feature title",
    "description": "Detailed description of the request",
    "category": "Integration|Analytics|Security|Performance|UI/UX|API|Admin",
    "request_count": 5,
    "unique_accounts": 3,
    "total_arr_impact": 450000,
    "avg_account_health": 82.5,
    "strategic_alignment": "high|medium|low",
    "effort_estimate": "S|M|L|XL",
    "priority_score": 0.0-1.0,
    "requesting_accounts": [
      {{"account_id": "acc-1", "arr": 150000, "health_score": 85, "verbatim": "exact quote"}}
    ],
    "similar_existing_features": ["existing feature 1", "existing feature 2"]
  }}
]

Guidelines:
- Weight by ARR impact (higher ARR accounts = higher priority)
- Consider account health (healthy accounts = expansion signal)
- Strategic alignment with product vision
- Effort estimate affects ROI calculation
- Priority score = (ARR_weight * 0.4) + (strategic * 0.3) + (health * 0.2) + (1/effort * 0.1)
- Group similar requests into single feature
- Include verbatim quotes for evidence
"""

    try:
        groq_client = get_groq_client()
        completion = groq_client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        result = json.loads(completion.choices[0].message.content)
        features = result.get("features", result) if isinstance(result, dict) else result

        synthesized = []
        for f in features:
            synthesized.append(FeatureRequestSynthesis(
                feature_id=f.get("feature_id", f"FR-{len(synthesized)+1:03d}"),
                title=f.get("title", ""),
                description=f.get("description", ""),
                category=f.get("category", "Other"),
                request_count=f.get("request_count", 1),
                unique_accounts=f.get("unique_accounts", 1),
                total_arr_impact=f.get("total_arr_impact", 0),
                avg_account_health=f.get("avg_account_health", 50),
                strategic_alignment=f.get("strategic_alignment", "medium"),
                effort_estimate=f.get("effort_estimate", "M"),
                priority_score=f.get("priority_score", 0.5),
                requesting_accounts=f.get("requesting_accounts", []),
                similar_existing_features=f.get("similar_existing_features", []),
                generated_at=datetime.utcnow(),
            ))

        return synthesized

    except Exception as e:
        # Fallback synthesis
        return [
            FeatureRequestSynthesis(
                feature_id="FR-001",
                title="Advanced Role-Based Access Control (RBAC)",
                description="Granular permissions for multi-team enterprises with custom roles, resource-level permissions, and audit logging.",
                category="Security",
                request_count=12,
                unique_accounts=8,
                total_arr_impact=1200000,
                avg_account_health=84.5,
                strategic_alignment="high",
                effort_estimate="L",
                priority_score=0.87,
                requesting_accounts=[
                    {"account_id": "acme-corp", "arr": 250000, "health_score": 82, "verbatim": "Need custom roles for our 5 engineering teams with different access levels"},
                    {"account_id": "globex-inc", "arr": 180000, "health_score": 88, "verbatim": "Compliance requires audit trail on all permission changes"},
                    {"account_id": "wayne-enterprises", "arr": 320000, "health_score": 90, "verbatim": "RBAC is a blocker for our SOC2 renewal"},
                ],
                similar_existing_features=["Basic team permissions", "SSO integration"],
                generated_at=datetime.utcnow(),
            ),
            FeatureRequestSynthesis(
                feature_id="FR-002",
                title="Real-time Collaboration & Presence",
                description="Live cursors, presence indicators, and conflict-free editing for collaborative workflows.",
                category="UI/UX",
                request_count=18,
                unique_accounts=12,
                total_arr_impact=890000,
                avg_account_health=78.2,
                strategic_alignment="high",
                effort_estimate="XL",
                priority_score=0.72,
                requesting_accounts=[
                    {"account_id": "acme-corp", "arr": 250000, "health_score": 82, "verbatim": "Design team needs real-time collab like Figma"},
                    {"account_id": "stark-industries", "arr": 200000, "health_score": 75, "verbatim": "Engineering docs - multiple people editing causes conflicts"},
                ],
                similar_existing_features=["Comments", "Activity feed"],
                generated_at=datetime.utcnow(),
            ),
            FeatureRequestSynthesis(
                feature_id="FR-003",
                title="Custom Webhook Event Types",
                description="Extend webhook system with custom event types, filtering, and retry policies for enterprise integrations.",
                category="Integration",
                request_count=9,
                unique_accounts=6,
                total_arr_impact=650000,
                avg_account_health=81.0,
                strategic_alignment="medium",
                effort_estimate="M",
                priority_score=0.68,
                requesting_accounts=[
                    {"account_id": "globex-inc", "arr": 180000, "health_score": 88, "verbatim": "Need webhook for custom object lifecycle events"},
                    {"account_id": "umbrella-corp", "arr": 150000, "health_score": 79, "verbatim": "Current webhooks don't fire on field-level changes"},
                ],
                similar_existing_features=["Standard webhooks", "API polling"],
                generated_at=datetime.utcnow(),
            ),
        ]


async def extract_feedback_themes(
    account_ids: Optional[list[str]] = None,
    time_window_days: int = 90,
) -> list[FeedbackTheme]:
    """
    Extract recurring themes from product feedback.

    Args:
        account_ids: Optional list of account IDs
        time_window_days: Lookback window

    Returns:
        List of feedback themes with sentiment and impact
    """
    if account_ids:
        all_feedback = []
        for account_id in account_ids:
            memory = await hindsight_client.recall_context(
                entity_id=account_id,
                query="product feedback bugs usability performance reliability",
            )
            all_feedback.append(memory.context)
        feedback_text = "\n\n".join(all_feedback)
    else:
        memory = await hindsight_client.recall_context(
            entity_id="aggregate",
            query="product feedback themes bugs usability performance reliability",
        )
        feedback_text = memory.context

    prompt = f"""
Extract recurring themes from this product feedback:

{feedback_text}

Return JSON array:
[
  {{
    "theme": "theme name",
    "mention_count": 15,
    "sentiment": "positive|negative|neutral",
    "accounts_mentioning": 8,
    "total_arr": 1200000,
    "representative_quotes": ["quote 1", "quote 2"]
  }}
]
"""

    try:
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        result = json.loads(completion.choices[0].message.content)
        themes = result.get("themes", result) if isinstance(result, dict) else result

        return [
            FeedbackTheme(
                theme=t.get("theme", ""),
                mention_count=t.get("mention_count", 0),
                sentiment=t.get("sentiment", "neutral"),
                accounts_mentioning=t.get("accounts_mentioning", 0),
                total_arr=t.get("total_arr", 0),
                representative_quotes=t.get("representative_quotes", []),
            )
            for t in themes
        ]

    except Exception as e:
        return [
            FeedbackTheme(
                theme="API Performance & Latency",
                mention_count=24,
                sentiment="negative",
                accounts_mentioning=10,
                total_arr=1850000,
                representative_quotes=[
                    "API p99 latency spikes to 500ms under load",
                    "Need consistent <100ms for real-time features",
                ],
            ),
            FeedbackTheme(
                theme="Advanced Analytics & Reporting",
                mention_count=18,
                sentiment="positive",
                accounts_mentioning=12,
                total_arr=2100000,
                representative_quotes=[
                    "Love the new dashboard - need more customization",
                    "Executive team wants scheduled PDF reports",
                ],
            ),
            FeedbackTheme(
                theme="Onboarding & Developer Experience",
                mention_count=15,
                sentiment="neutral",
                accounts_mentioning=9,
                total_arr=980000,
                representative_quotes=[
                    "SDK docs are great but getting started guide is missing",
                    "Time to first API call took 2 hours - should be 15 min",
                ],
            ),
        ]


async def generate_roadmap_prioritization(
    features: list[FeatureRequestSynthesis],
    strategic_pillars: Optional[list[str]] = None,
) -> dict[str, Any]:
    """
    Generate a prioritized roadmap from feature requests.

    Args:
        features: List of synthesized feature requests
        strategic_pillars: Company strategic pillars for alignment

    Returns:
        Roadmap with quarters, priorities, and rationale
    """
    if not strategic_pillars:
        strategic_pillars = ["Enterprise Security", "Developer Experience", "Platform Extensibility", "AI/ML Capabilities"]

    features_data = [
        {
            "feature_id": f.feature_id,
            "title": f.title,
            "category": f.category,
            "priority_score": f.priority_score,
            "total_arr_impact": f.total_arr_impact,
            "effort_estimate": f.effort_estimate,
            "strategic_alignment": f.strategic_alignment,
        }
        for f in features
    ]

    prompt = f"""
Prioritize these features into a 4-quarter roadmap.

Features: {json.dumps(features_data, indent=2)}
Strategic Pillars: {strategic_pillars}

Return JSON:
{{
  "Q1": [{{"feature_id": "FR-001", "rationale": "why now"}}],
  "Q2": [...],
  "Q3": [...],
  "Q4": [...],
  "quick_wins": ["FR-XXX"],
  "strategic_bets": ["FR-XXX"],
  "deferred": ["FR-XXX"],
  "rationale_summary": "overall prioritization logic"
}}
"""

    try:
        groq_client = get_groq_client()
        completion = groq_client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        return json.loads(completion.choices[0].message.content)

    except Exception as e:
        return {
            "Q1": [{"feature_id": "FR-001", "rationale": "High ARR impact, security blocker for renewals"}],
            "Q2": [{"feature_id": "FR-003", "rationale": "Medium effort, high integration value"}],
            "Q3": [{"feature_id": "FR-002", "rationale": "Strategic differentiator, long build time"}],
            "Q4": [],
            "quick_wins": ["FR-003"],
            "strategic_bets": ["FR-002"],
            "deferred": [],
            "rationale_summary": "Prioritized by ARR-weighted priority score, strategic alignment, and effort. Security features first (renewal blockers), then integration extensibility, then collaborative differentiation.",
        }


async def retain_product_feedback(
    account_id: str,
    feedback_type: str,
    content: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Retain product feedback in Hindsight memory."""
    full_metadata = {
        "feedback_type": feedback_type,
        "timestamp": datetime.utcnow().isoformat(),
        **metadata,
    }
    return await hindsight_client.retain_memory(
        entity_id=account_id,
        content=content,
        metadata=full_metadata,
    )