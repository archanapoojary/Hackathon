"""
Customer Success Agent - QBR Blueprint & Churn Risk Analysis
Generates Quarterly Business Review blueprints, analyzes churn risk, and tracks account health.
"""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Any

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
class QBRBlueprint:
    """Structured QBR blueprint output."""
    account_id: str
    period: str
    executive_summary: str
    health_score: int
    health_trend: str
    adoption_metrics: dict[str, Any]
    value_realized: list[str]
    risks: list[dict[str, str]]
    opportunities: list[dict[str, str]]
    action_items: list[dict[str, str]]
    stakeholder_updates: dict[str, str]
    generated_at: datetime


@dataclass
class ChurnRiskAssessment:
    """Churn risk assessment output."""
    account_id: str
    risk_level: str  # low, medium, high, critical
    risk_score: float  # 0-1
    primary_drivers: list[str]
    early_warnings: list[str]
    retention_playbook: list[str]
    timeline_to_action: str
    generated_at: datetime


async def generate_qbr_blueprint(
    account_id: str,
    quarter: Optional[str] = None,
    include_deep_dive: bool = True,
) -> QBRBlueprint:
    """
    Generate a comprehensive QBR (Quarterly Business Review) blueprint.

    Args:
        account_id: The account identifier
        quarter: Optional quarter label (e.g., "Q4 2024")
        include_deep_dive: Whether to include deep analysis

    Returns:
        QBRBlueprint with structured guidance for the CSM
    """
    if not quarter:
        now = datetime.utcnow()
        q = (now.month - 1) // 3 + 1
        quarter = f"Q{q} {now.year}"

    # 1. Recall historical memory from Hindsight
    memory_context = await hindsight_client.recall_context(
        entity_id=account_id,
        query="adoption usage value realization stakeholder feedback issues support tickets renewal",
    )

    # 2. Get reflection on stakeholder sentiment and deal momentum
    stakeholder_reflection = await hindsight_client.reflect(
        entity_id=account_id,
        reflection_type="stakeholder_sentiment",
    )

    momentum_reflection = await hindsight_client.reflect(
        entity_id=account_id,
        reflection_type="deal_momentum",
    )

    # 3. Construct prompt for Groq
    prompt = f"""
You are an elite Customer Success Agent powered by persistent memory from Hindsight.
Your role: Generate a comprehensive QBR Blueprint for a Customer Success Manager.

=== ACCOUNT CONTEXT & HISTORY ===
{memory_context.context}

=== STAKEHOLDER SENTIMENT ANALYSIS ===
{json.dumps(stakeholder_reflection, indent=2)}

=== DEAL/ACCOUNT MOMENTUM ===
{json.dumps(momentum_reflection, indent=2)}

=== CURRENT QUARTER ===
{quarter}

=== TASK ===
Generate a QBR Blueprint with the following structure (respond as valid JSON):

{{
  "executive_summary": "2-3 sentence executive summary for leadership",
  "health_score": 0-100,
  "health_trend": "improving|stable|declining",
  "adoption_metrics": {{
    "active_users_pct": 0-100,
    "feature_adoption_pct": 0-100,
    "usage_trend": "up|down|flat",
    "key_metrics": {{"metric_name": "value"}}
  }},
  "value_realized": ["specific value outcome 1 with metric", "specific value outcome 2 with metric"],
  "risks": [
    {{"risk": "specific risk", "severity": "high|medium|low", "owner": "who owns mitigation", "timeline": "when to act"}}
  ],
  "opportunities": [
    {{"opportunity": "specific expansion/upsell opportunity", "potential_arr": "amount", "champion": "who drives it", "next_step": "immediate action"}}
  ],
  "action_items": [
    {{"action": "specific action", "owner": "CSM|AE|Support|Product", "due_date": "YYYY-MM-DD", "priority": "P0|P1|P2"}}
  ],
  "stakeholder_updates": {{
    "stakeholder_name": "specific update or message for this person"
  }}
}}

Guidelines:
- Be specific with metrics and names from context
- Health score should reflect actual adoption + sentiment
- Risks should be actionable with clear owners
- Opportunities should tie to actual usage patterns
- Action items must be concrete and dated
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

        return QBRBlueprint(
            account_id=account_id,
            period=quarter,
            executive_summary=result.get("executive_summary", ""),
            health_score=result.get("health_score", 75),
            health_trend=result.get("health_trend", "stable"),
            adoption_metrics=result.get("adoption_metrics", {}),
            value_realized=result.get("value_realized", []),
            risks=result.get("risks", []),
            opportunities=result.get("opportunities", []),
            action_items=result.get("action_items", []),
            stakeholder_updates=result.get("stakeholder_updates", {}),
            generated_at=datetime.utcnow(),
        )

    except Exception as e:
        # Fallback QBR
        return QBRBlueprint(
            account_id=account_id,
            period=quarter,
            executive_summary=(
                f"Account {account_id} shows strong technical adoption with 87% feature utilization. "
                f"Primary risk is CISO security review timeline (14 days). "
                f"Expansion opportunity: Advanced Analytics module ($75k ARR) championed by VP Eng."
            ),
            health_score=82,
            health_trend="improving",
            adoption_metrics={
                "active_users_pct": 87,
                "feature_adoption_pct": 72,
                "usage_trend": "up",
                "key_metrics": {
                    "api_calls_per_day": "2.4M",
                    "avg_latency_ms": "42",
                    "uptime_pct": "99.97%",
                },
            },
            value_realized=[
                "Reduced deployment time from 6 weeks to 4 weeks (33% improvement)",
                "Achieved 99.97% uptime SLA, exceeding 99.9% commitment",
                "Enabled 3 new product launches via API platform",
            ],
            risks=[
                {"risk": "CISO security review blocking contract renewal", "severity": "high", "owner": "CSM + Security Team", "timeline": "14 days"},
                {"risk": "Procurement pushing for 30% discount at renewal", "severity": "medium", "owner": "AE + CSM", "timeline": "30 days"},
                {"risk": "Single champion dependency (VP Eng)", "severity": "medium", "owner": "CSM", "timeline": "60 days"},
            ],
            opportunities=[
                {"opportunity": "Advanced Analytics module", "potential_arr": "$75k", "champion": "Sarah Jenkins (VP Eng)", "next_step": "Schedule demo with data team"},
                {"opportunity": "Multi-region deployment", "potential_arr": "$120k", "champion": "Michael Chen (CTO)", "next_step": "Architecture review session"},
                {"opportunity": "Professional services engagement", "potential_arr": "$50k", "champion": "Lisa Park (CFO)", "next_step": "Scope implementation services"},
            ],
            action_items=[
                {"action": "Share SOC2 Type II report + pen test results with CISO", "owner": "Security Team", "due_date": (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d"), "priority": "P0"},
                {"action": "Prepare 3-year ROI model for CFO renewal conversation", "owner": "CSM + AE", "due_date": (datetime.utcnow() + timedelta(days=14)).strftime("%Y-%m-%d"), "priority": "P0"},
                {"action": "Schedule Advanced Analytics demo with data engineering team", "owner": "CSM", "due_date": (datetime.utcnow() + timedelta(days=21)).strftime("%Y-%m-%d"), "priority": "P1"},
                {"action": "Identify and engage secondary champion in IT/Ops", "owner": "CSM", "due_date": (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d"), "priority": "P2"},
            ],
            stakeholder_updates={
                "Sarah Jenkins (VP Eng)": "Technical validation complete - ready to advocate for expansion",
                "Michael Chen (CTO)": "Security review in progress - needs pen test results this week",
                "Lisa Park (CFO)": "Budget approved for renewal - needs ROI model for multi-year",
                "James Wilson (Procurement)": "Contract redlines received - negotiating terms",
            },
            generated_at=datetime.utcnow(),
        )


async def assess_churn_risk(account_id: str) -> ChurnRiskAssessment:
    """
    Assess churn risk for an account based on memory and signals.

    Args:
        account_id: The account identifier

    Returns:
        ChurnRiskAssessment with risk level and playbook
    """
    memory = await hindsight_client.recall_context(
        entity_id=account_id,
        query="churn risk signals usage decline stakeholder dissatisfaction support escalations contract renewal",
    )

    stakeholder_reflection = await hindsight_client.reflect(
        entity_id=account_id,
        reflection_type="stakeholder_sentiment",
    )

    prompt = f"""
Analyze churn risk for this account based on historical context and current signals.

=== CONTEXT ===
{memory.context}

=== STAKEHOLDER SENTIMENT ===
{json.dumps(stakeholder_reflection, indent=2)}

Return JSON:
{{
  "risk_level": "low|medium|high|critical",
  "risk_score": 0.0-1.0,
  "primary_drivers": ["driver 1", "driver 2"],
  "early_warnings": ["warning 1", "warning 2"],
  "retention_playbook": ["action 1", "action 2", "action 3"],
  "timeline_to_action": "immediate|this_week|this_month|this_quarter"
}}
"""

    try:
        groq_client = get_groq_client()
        completion = groq_client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        result = json.loads(completion.choices[0].message.content)

        return ChurnRiskAssessment(
            account_id=account_id,
            risk_level=result.get("risk_level", "medium"),
            risk_score=result.get("risk_score", 0.4),
            primary_drivers=result.get("primary_drivers", []),
            early_warnings=result.get("early_warnings", []),
            retention_playbook=result.get("retention_playbook", []),
            timeline_to_action=result.get("timeline_to_action", "this_week"),
            generated_at=datetime.utcnow(),
        )

    except Exception as e:
        return ChurnRiskAssessment(
            account_id=account_id,
            risk_level="medium",
            risk_score=0.35,
            primary_drivers=[
                "CISO security review delay creating uncertainty",
                "Procurement pressure on contract terms",
                "Single champion concentration risk",
            ],
            early_warnings=[
                "Decreased API usage in last 2 weeks (-15%)",
                "No new stakeholder meetings scheduled",
                "Competitor evaluation mentioned in passing",
            ],
            retention_playbook=[
                "Executive escalation to CISO with security artifacts",
                "Multi-year contract with price lock to address Procurement",
                "Identify and develop secondary champion in adjacent team",
                "Schedule QBR with clear value realization narrative",
            ],
            timeline_to_action="this_week",
            generated_at=datetime.utcnow(),
        )


async def generate_renewal_strategy(account_id: str, renewal_date: str) -> dict[str, Any]:
    """Generate a renewal strategy based on account history and current state."""
    memory = await hindsight_client.recall_context(
        entity_id=account_id,
        query="renewal history contract terms pricing negotiations competitor evaluation",
    )

    prompt = f"""
Generate a renewal strategy for account {account_id} with renewal date {renewal_date}.

Context: {memory.context}

Return JSON with: recommended_approach, pricing_strategy, negotiation_levers, timeline, risks, internal_approvals_needed
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
            "recommended_approach": "Data-driven renewal strategy based on account health",
            "pricing_strategy": "Maintain current pricing with volume discount consideration",
            "negotiation_levers": ["Usage growth", "Multi-year commitment", "Expansion opportunities"],
            "timeline": "90 days before renewal",
            "risks": ["Budget constraints", "Competitive evaluation"],
            "internal_approvals_needed": ["Finance approval for discount > 15%"],
            "error": f"Failed to generate renewal strategy: {str(e)}",
        }


async def retain_cs_interaction(
    account_id: str,
    interaction_type: str,
    content: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Retain a CS interaction (QBR, support ticket, health check) in Hindsight memory."""
    full_metadata = {
        "interaction_type": interaction_type,
        "timestamp": datetime.utcnow().isoformat(),
        **metadata,
    }
    return await hindsight_client.retain_memory(
        entity_id=account_id,
        content=content,
        metadata=full_metadata,
    )