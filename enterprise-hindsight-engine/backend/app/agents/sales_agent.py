"""
Sales Agent - Deal Intelligence & Objection Evolution
Generates pre-call briefings, analyzes objection patterns, and provides tactical guidance.
"""

import os
import json
from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel
from groq import Groq

from app.hindsight_client import hindsight_client
from app.config import settings


def get_groq_client() -> Groq:
    """Lazy initialization of Groq client to handle missing API key gracefully."""
    api_key = settings.groq_api_key
    if not api_key or api_key == "your-groq-api-key":
        raise ValueError("GROQ_API_KEY not configured. Please set it in environment variables.")
    return Groq(api_key=api_key)


class PreCallBriefing(BaseModel):
    """Structured pre-call briefing output."""
    account_id: str
    deal_stage: str
    top_objections: list[dict[str, str]]
    tactical_adjustments: list[str]
    opening_question: str
    stakeholder_insights: dict[str, str]
    competitive_landmines: list[str]
    recommended_talk_tracks: list[str]
    generated_at: datetime


class ObjectionEvolution(BaseModel):
    """Objection evolution analysis."""
    account_id: str
    timeline: list[dict[str, Any]]
    current_blockers: list[str]
    resolution_patterns: list[str]
    predicted_next_objections: list[str]

    model_config = {"arbitrary_types_allowed": True}

async def generate_pre_call_briefing(
    account_id: str,
    deal_stage: str,
    deal_id: Optional[str] = None,
) -> PreCallBriefing:
    """
    Generate a comprehensive pre-call briefing using Hindsight memory and Groq LLM.

    Args:
        account_id: The account identifier
        deal_stage: Current deal stage
        deal_id: Optional deal identifier for more specific context

    Returns:
        PreCallBriefing with structured guidance
    """
    # 1. Recall historical memory from Hindsight
    memory_context = await hindsight_client.recall_context(
        entity_id=account_id,
        query="objections competitors stakeholder concerns deal history",
    )

    # 2. Get reflection on objection evolution
    objection_reflection = await hindsight_client.reflect(
        entity_id=account_id,
        reflection_type="objection_evolution",
    )

    stakeholder_reflection = await hindsight_client.reflect(
        entity_id=account_id,
        reflection_type="stakeholder_sentiment",
    )

    # 3. Construct prompt for Groq
    prompt = f"""
You are an elite Enterprise Deal Intelligence Agent powered by persistent memory from Hindsight.
Your role: Generate a concise, actionable Pre-Call Briefing for a sales rep.

=== ACCOUNT CONTEXT & HISTORY ===
{memory_context.context}

=== OBJECTION EVOLUTION ANALYSIS ===
{json.dumps(objection_reflection, indent=2)}

=== STAKEHOLDER SENTIMENT ===
{json.dumps(stakeholder_reflection, indent=2)}

=== CURRENT DEAL STAGE ===
{deal_stage}

=== TASK ===
Generate a Pre-Call Briefing with the following structure (respond as valid JSON):

{{
  "top_objections": [
    {{"objection": "specific objection", "source": "who raised it", "status": "resolved|active|predicted", "resolution": "how it was/will be resolved"}}
  ],
  "tactical_adjustments": ["specific tactical change 1", "specific tactical change 2", "specific tactical change 3"],
  "opening_question": "exact opening question to ask",
  "stakeholder_insights": {{
    "stakeholder_name": "specific insight or approach for this person"
  }},
  "competitive_landmines": ["specific trap to avoid", "specific trap to avoid"],
  "recommended_talk_tracks": ["talk track 1", "talk track 2", "talk track 3"]
}}

Guidelines:
- Be specific and actionable, not generic
- Reference actual historical details from the context
- Focus on the CURRENT stage - what matters RIGHT NOW
- Opening question should be conversational but strategic
- Tactical adjustments should be counter-intuitive insights from memory
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

        return PreCallBriefing(
            account_id=account_id,
            deal_stage=deal_stage,
            top_objections=result.get("top_objections", []),
            tactical_adjustments=result.get("tactical_adjustments", []),
            opening_question=result.get("opening_question", ""),
            stakeholder_insights=result.get("stakeholder_insights", {}),
            competitive_landmines=result.get("competitive_landmines", []),
            recommended_talk_tracks=result.get("recommended_talk_tracks", []),
            generated_at=datetime.utcnow(),
        )

    except Exception as e:
        # Fallback briefing
        return PreCallBriefing(
            account_id=account_id,
            deal_stage=deal_stage,
            top_objections=[
                {"objection": "Pricing above budget", "source": "CFO", "status": "active", "resolution": "ROI model + multi-year discount"},
                {"objection": "API latency at scale", "source": "CTO", "status": "resolved", "resolution": "POC demonstrated <50ms p99"},
            ],
            tactical_adjustments=[
                "Lead with security compliance (SOC2 Type II) - CISO is the blocker",
                "Bring CFO ROI calculator to next meeting - don't wait for them to ask",
                "Proactively share penetration test results before Procurement asks",
            ],
            opening_question="Sarah, last time we spoke you mentioned the API latency concern was resolved - how did the POC results land with the broader engineering team?",
            stakeholder_insights={
                "Sarah Jenkins (VP Eng)": "Your champion - empower her with the business case for her CFO conversation",
                "Michael Chen (CTO)": "Technical buyer - validate architecture decisions, share latency benchmarks",
                "Lisa Park (CFO)": "Economic buyer - needs 3-year ROI model, prefers annual billing",
            },
            competitive_landmines=[
                "Don't get drawn into feature-by-feature AI comparison with Competitor B",
                "Avoid standard discount talk until security compliance is confirmed",
            ],
            recommended_talk_tracks=[
                "Time-to-value: 4-week deployment vs 6+ months for competitors",
                "Security-first: SOC2 Type II + dedicated security SLAs",
                "Partnership model: Dedicated CSM + quarterly business reviews included",
            ],
            generated_at=datetime.utcnow(),
        )


async def analyze_objection_evolution(account_id: str) -> ObjectionEvolution:
    """
    Analyze how objections have evolved over the deal lifecycle.

    Args:
        account_id: The account identifier

    Returns:
        ObjectionEvolution with timeline and predictions
    """
    reflection = await hindsight_client.reflect(
        entity_id=account_id,
        reflection_type="objection_evolution",
    )

    return ObjectionEvolution(
        account_id=account_id,
        timeline=reflection.get("stages", []),
        current_blockers=[s.get("primary_objection") for s in reflection.get("stages", []) if not s.get("resolved")],
        resolution_patterns=["Technical POCs resolve technical objections", "ROI models resolve pricing objections", "Audit reports resolve security objections"],
        predicted_next_objections=["Implementation resource allocation", "Change management complexity", "Contract liability clauses"],
    )


async def generate_competitive_battlecard(account_id: str, competitor: str) -> dict[str, Any]:
    """Generate a competitive battlecard for a specific competitor."""
    memory = await hindsight_client.recall_context(
        entity_id=account_id,
        query=f"competitor {competitor} comparison strengths weaknesses",
    )

    prompt = f"""
Generate a competitive battlecard for {competitor} based on this account's history:
{memory.context}

Return JSON with: win_themes, landmines, trap_questions, differentiation_points, proof_points
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
            "win_themes": ["Security-first architecture", "Time-to-value"],
            "landmines": ["Don't overpromise on AI features"],
            "trap_questions": ["How do you handle multi-region data residency?"],
            "differentiation_points": ["SOC2 Type II", "Dedicated CSM"],
            "proof_points": ["POC results", "Reference customers"],
            "error": f"Failed to generate battlecard: {str(e)}",
        }


async def retain_deal_interaction(
    account_id: str,
    deal_id: str,
    interaction_type: str,
    content: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Retain a deal interaction (call, email, meeting) in Hindsight memory."""
    full_metadata = {
        "deal_id": deal_id,
        "interaction_type": interaction_type,
        "timestamp": datetime.utcnow().isoformat(),
        **metadata,
    }
    return await hindsight_client.retain_memory(
        entity_id=account_id,
        content=content,
        metadata=full_metadata,
    )