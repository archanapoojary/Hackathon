"""
Sales Deals Router - API endpoints for deal intelligence.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.agents.sales_agent import (
    generate_pre_call_briefing,
    analyze_objection_evolution,
    generate_competitive_battlecard,
    retain_deal_interaction,
    PreCallBriefing,
    ObjectionEvolution,
)

router = APIRouter()


class DealInteractionRequest(BaseModel):
    deal_id: str
    interaction_type: str = Field(..., description="call, email, meeting, demo, proposal")
    content: str
    metadata: dict = Field(default_factory=dict)


class CompetitiveBattlecardRequest(BaseModel):
    competitor: str


@router.get("/health")
async def deals_health():
    """Health check for deals router."""
    return {"status": "healthy", "service": "deals", "timestamp": datetime.utcnow().isoformat()}


@router.post("/briefing/{account_id}", response_model=PreCallBriefing)
async def get_pre_call_briefing(
    account_id: str = Path(..., description="Account identifier"),
    deal_stage: str = Query(..., description="Current deal stage"),
    deal_id: Optional[str] = Query(None, description="Optional deal identifier"),
):
    """
    Generate a pre-call briefing for a sales call.
    
    Uses Hindsight memory to recall historical context, objection evolution,
    and stakeholder sentiment, then generates tactical guidance via Groq.
    """
    try:
        briefing = await generate_pre_call_briefing(
            account_id=account_id,
            deal_stage=deal_stage,
            deal_id=deal_id,
        )
        return briefing
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate briefing: {str(e)}")


@router.get("/objection-evolution/{account_id}", response_model=ObjectionEvolution)
async def get_objection_evolution(
    account_id: str = Path(..., description="Account identifier"),
):
    """
    Analyze how objections have evolved over the deal lifecycle.
    
    Returns timeline, current blockers, resolution patterns, and predictions.
    """
    try:
        evolution = await analyze_objection_evolution(account_id)
        return evolution
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze objections: {str(e)}")


@router.post("/battlecard/{account_id}")
async def get_competitive_battlecard(
    account_id: str = Path(..., description="Account identifier"),
    request: CompetitiveBattlecardRequest = None,
):
    """
    Generate a competitive battlecard for a specific competitor.
    
    Provides win themes, landmines, trap questions, and differentiation points.
    """
    if not request or not request.competitor:
        raise HTTPException(status_code=400, detail="Competitor name required")
    
    try:
        battlecard = await generate_competitive_battlecard(account_id, request.competitor)
        return battlecard
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate battlecard: {str(e)}")


@router.post("/interaction/{account_id}")
async def record_deal_interaction(
    account_id: str = Path(..., description="Account identifier"),
    request: DealInteractionRequest = None,
):
    """
    Record a deal interaction (call, email, meeting, etc.) in Hindsight memory.
    
    This builds the persistent memory that powers future briefings.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Interaction data required")
    
    try:
        result = await retain_deal_interaction(
            account_id=account_id,
            deal_id=request.deal_id,
            interaction_type=request.interaction_type,
            content=request.content,
            metadata=request.metadata,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record interaction: {str(e)}")


@router.get("/stages")
async def get_deal_stages():
    """Get standard deal stages for reference."""
    return {
        "stages": [
            "Prospecting",
            "Discovery",
            "Technical Validation",
            "Proof of Concept",
            "Security Review",
            "Negotiation",
            "Contract Review",
            "Closed Won",
            "Closed Lost",
        ],
        "typical_progression": [
            "Prospecting → Discovery → Technical Validation",
            "Technical Validation → POC → Security Review",
            "Security Review → Negotiation → Contract Review → Closed Won",
        ],
    }


@router.get("/objection-playbook")
async def get_objection_playbook():
    """Get common objection handling playbook."""
    return {
        "common_objections": [
            {
                "category": "Pricing",
                "objections": [
                    "Too expensive / budget constraints",
                    "Competitor is cheaper",
                    "Need discount / better terms",
                    "ROI unclear",
                ],
                "responses": [
                    "Multi-year discount + price lock",
                    "ROI calculator with customer-specific metrics",
                    "Phased rollout to reduce upfront cost",
                    "Value comparison vs. build vs. competitor",
                ],
            },
            {
                "category": "Technical",
                "objections": [
                    "API latency / performance concerns",
                    "Integration complexity",
                    "Scalability doubts",
                    "Vendor lock-in fears",
                ],
                "responses": [
                    "POC with production-like load",
                    "Architecture deep-dive with engineering",
                    "Reference customers at similar scale",
                    "Open APIs, standard protocols, data portability",
                ],
            },
            {
                "category": "Security",
                "objections": [
                    "SOC2 Type II required",
                    "Data residency / compliance",
                    "Penetration test results needed",
                    "Vendor security questionnaire",
                ],
                "responses": [
                    "Proactive security package sharing",
                    "Compliance certifications portfolio",
                    "Third-party audit reports",
                    "Security addendum to contract",
                ],
            },
            {
                "category": "Procurement",
                "objections": [
                    "Need 3 quotes",
                    "Standard contract terms only",
                    "Net-60 / Net-90 payment terms",
                    "Auto-renewal clause removal",
                ],
                "responses": [
                    "Executive sponsorship for exception",
                    "MSA template pre-review",
                    "Value-based pricing justification",
                    "Multi-year commitment for favorable terms",
                ],
            },
        ],
    }