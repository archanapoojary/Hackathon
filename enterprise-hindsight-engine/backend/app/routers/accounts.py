"""
Customer Success Accounts Router - API endpoints for QBR, churn risk, renewals.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.agents.cs_agent import (
    generate_qbr_blueprint,
    assess_churn_risk,
    generate_renewal_strategy,
    retain_cs_interaction,
    QBRBlueprint,
    ChurnRiskAssessment,
)

router = APIRouter()


class CSInteractionRequest(BaseModel):
    interaction_type: str = Field(..., description="qbr, health_check, support_escalation, stakeholder_meeting")
    content: str
    metadata: dict = Field(default_factory=dict)


class RenewalStrategyRequest(BaseModel):
    renewal_date: str = Field(..., description="ISO format date string")


@router.get("/health")
async def accounts_health():
    """Health check for accounts router."""
    return {"status": "healthy", "service": "accounts", "timestamp": datetime.utcnow().isoformat()}


@router.post("/qbr/{account_id}", response_model=QBRBlueprint)
async def get_qbr_blueprint(
    account_id: str = Path(..., description="Account identifier"),
    quarter: Optional[str] = Query(None, description="Quarter label (e.g., Q4 2024)"),
    deep_dive: bool = Query(True, description="Include deep analysis"),
):
    """
    Generate a comprehensive QBR (Quarterly Business Review) blueprint.
    
    Includes executive summary, health score, adoption metrics, value realized,
    risks, opportunities, action items, and stakeholder updates.
    """
    try:
        qbr = await generate_qbr_blueprint(
            account_id=account_id,
            quarter=quarter,
            include_deep_dive=deep_dive,
        )
        return qbr
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QBR: {str(e)}")


@router.get("/churn-risk/{account_id}", response_model=ChurnRiskAssessment)
async def get_churn_risk(
    account_id: str = Path(..., description="Account identifier"),
):
    """
    Assess churn risk for an account.
    
    Returns risk level, primary drivers, early warnings, and retention playbook.
    """
    try:
        risk = await assess_churn_risk(account_id)
        return risk
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assess churn risk: {str(e)}")


@router.post("/renewal-strategy/{account_id}")
async def get_renewal_strategy(
    account_id: str = Path(..., description="Account identifier"),
    request: RenewalStrategyRequest = None,
):
    """
    Generate a renewal strategy for an upcoming contract renewal.
    
    Includes recommended approach, pricing strategy, negotiation levers, and timeline.
    """
    if not request or not request.renewal_date:
        raise HTTPException(status_code=400, detail="Renewal date required")
    
    try:
        strategy = await generate_renewal_strategy(account_id, request.renewal_date)
        return strategy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate renewal strategy: {str(e)}")


@router.post("/interaction/{account_id}")
async def record_cs_interaction(
    account_id: str = Path(..., description="Account identifier"),
    request: CSInteractionRequest = None,
):
    """
    Record a CS interaction (QBR, health check, support escalation) in Hindsight memory.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Interaction data required")
    
    try:
        result = await retain_cs_interaction(
            account_id=account_id,
            interaction_type=request.interaction_type,
            content=request.content,
            metadata=request.metadata,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record interaction: {str(e)}")


@router.get("/health-scoring")
async def get_health_scoring_methodology():
    """Get the health scoring methodology for reference."""
    return {
        "health_score_components": [
            {"component": "Product Adoption", "weight": 0.35, "metrics": ["Active users %", "Feature adoption %", "Usage frequency", "Depth of usage"]},
            {"component": "Value Realization", "weight": 0.25, "metrics": ["ROI achieved", "Business outcomes", "Time to value", "Expansion usage"]},
            {"component": "Stakeholder Sentiment", "weight": 0.20, "metrics": ["NPS/CSAT", "Champion engagement", "Decision maker access", "Sentiment trend"]},
            {"component": "Operational Health", "weight": 0.20, "metrics": ["Support ticket volume", "SLA compliance", "Onboarding completion", "Training adoption"]},
        ],
        "score_bands": [
            {"range": "90-100", "label": "Champion", "color": "green", "action": "Advocate & expand"},
            {"range": "75-89", "label": "Healthy", "color": "blue", "action": "Nurture & grow"},
            {"range": "60-74", "label": "At Risk", "color": "yellow", "action": "Intervene & recover"},
            {"range": "0-59", "label": "Critical", "color": "red", "action": "Executive escalation"},
        ],
        "trend_indicators": {
            "improving": "Score increased >5 points or positive momentum in 2+ components",
            "stable": "Score within ±5 points, no major component shifts",
            "declining": "Score decreased >5 points or negative momentum in 2+ components",
        },
    }


@router.get("/qbr-template")
async def get_qbr_template():
    """Get standard QBR template structure."""
    return {
        "sections": [
            {"id": "executive_summary", "title": "Executive Summary", "audience": "Leadership", "duration_min": 5},
            {"id": "health_score", "title": "Account Health Score", "audience": "All", "duration_min": 10},
            {"id": "adoption_metrics", "title": "Product Adoption & Usage", "audience": "Technical/CS", "duration_min": 15},
            {"id": "value_realized", "title": "Value Realization & ROI", "audience": "Business/Economic Buyer", "duration_min": 15},
            {"id": "strategic_alignment", "title": "Strategic Alignment & Roadmap", "audience": "Decision Makers", "duration_min": 10},
            {"id": "risks_mitigations", "title": "Risks & Mitigations", "audience": "All", "duration_min": 10},
            {"id": "opportunities", "title": "Expansion Opportunities", "audience": "Sales/CS/Leadership", "duration_min": 10},
            {"id": "action_items", "title": "Action Items & Owners", "audience": "All", "duration_min": 5},
        ],
        "total_duration_min": 80,
        "preparation_checklist": [
            "Pull latest usage analytics",
            "Review support ticket trends",
            "Check stakeholder meeting notes",
            "Prepare ROI calculations",
            "Align with AE on expansion plays",
            "Review product roadmap for relevance",
        ],
    }