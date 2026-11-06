"""
Product Feedback Router - API endpoints for feature synthesis and roadmap.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.agents.product_agent import (
    synthesize_feature_requests,
    extract_feedback_themes,
    generate_roadmap_prioritization,
    retain_product_feedback,
    FeatureRequestSynthesis,
    FeedbackTheme,
)

router = APIRouter()


class ProductFeedbackRequest(BaseModel):
    feedback_type: str = Field(..., description="feature_request, bug_report, usability_issue, improvement, praise")
    content: str
    metadata: dict = Field(default_factory=dict)


class RoadmapRequest(BaseModel):
    strategic_pillars: Optional[List[str]] = None


@router.get("/health")
async def feedback_health():
    """Health check for feedback router."""
    return {"status": "healthy", "service": "feedback", "timestamp": datetime.utcnow().isoformat()}


@router.post("/synthesize", response_model=List[FeatureRequestSynthesis])
async def synthesize_features(
    account_ids: Optional[List[str]] = Query(None, description="List of account IDs to analyze"),
    time_window_days: int = Query(90, ge=1, le=365, description="Lookback window in days"),
    min_arr_threshold: float = Query(0, ge=0, description="Minimum ARR threshold for accounts"),
):
    """
    Synthesize and prioritize feature requests from multiple accounts.
    
    Weights requests by ARR impact, account health, strategic alignment, and effort.
    Returns prioritized list with revenue-weighted priority scores.
    """
    try:
        features = await synthesize_feature_requests(
            account_ids=account_ids,
            time_window_days=time_window_days,
            min_arr_threshold=min_arr_threshold,
        )
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to synthesize features: {str(e)}")


@router.get("/themes", response_model=List[FeedbackTheme])
async def get_feedback_themes(
    account_ids: Optional[List[str]] = Query(None, description="List of account IDs to analyze"),
    time_window_days: int = Query(90, ge=1, le=365, description="Lookback window in days"),
):
    """
    Extract recurring themes from product feedback across accounts.
    
    Returns themes with sentiment, mention count, ARR impact, and representative quotes.
    """
    try:
        themes = await extract_feedback_themes(
            account_ids=account_ids,
            time_window_days=time_window_days,
        )
        return themes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract themes: {str(e)}")


@router.post("/roadmap")
async def generate_roadmap(
    request: RoadmapRequest = None,
    account_ids: Optional[List[str]] = Query(None, description="Accounts to base roadmap on"),
    time_window_days: int = Query(90, ge=1, le=365),
):
    """
    Generate a prioritized product roadmap from synthesized feature requests.
    
    Organizes features into quarters with rationale, identifies quick wins and strategic bets.
    """
    try:
        # First synthesize features
        features = await synthesize_feature_requests(
            account_ids=account_ids,
            time_window_days=time_window_days,
        )
        
        # Then generate roadmap
        strategic_pillars = request.strategic_pillars if request else None
        roadmap = await generate_roadmap_prioritization(features, strategic_pillars)
        
        return {
            "features_analyzed": len(features),
            "roadmap": roadmap,
            "generated_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate roadmap: {str(e)}")


@router.post("/feedback/{account_id}")
async def submit_product_feedback(
    account_id: str = Path(..., description="Account identifier"),
    request: ProductFeedbackRequest = None,
):
    """
    Submit product feedback for an account.
    
    Stores in Hindsight memory for future synthesis and roadmap planning.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Feedback data required")
    
    try:
        result = await retain_product_feedback(
            account_id=account_id,
            feedback_type=request.feedback_type,
            content=request.content,
            metadata=request.metadata,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")


@router.get("/categories")
async def get_feedback_categories():
    """Get standard feedback categories for reference."""
    return {
        "feedback_types": [
            {"id": "feature_request", "label": "Feature Request", "description": "New capability or enhancement"},
            {"id": "bug_report", "label": "Bug Report", "description": "Defect or unexpected behavior"},
            {"id": "usability_issue", "label": "Usability Issue", "description": "Confusing, difficult, or frustrating UX"},
            {"id": "improvement", "label": "Improvement", "description": "Enhancement to existing feature"},
            {"id": "praise", "label": "Praise / Positive Feedback", "description": "What's working well"},
        ],
        "categories": [
            "Integration",
            "Analytics",
            "Security",
            "Performance",
            "UI/UX",
            "API",
            "Admin",
            "Mobile",
            "AI/ML",
            "Compliance",
            "Billing",
            "Onboarding",
        ],
        "effort_estimates": {
            "S": "1-2 weeks (small, well-scoped)",
            "M": "3-6 weeks (medium, some unknowns)",
            "L": "2-3 months (large, significant engineering)",
            "XL": "3+ months (major initiative, cross-team)",
        },
    }


@router.get("/priority-framework")
async def get_priority_framework():
    """Get the prioritization framework used for roadmap decisions."""
    return {
        "priority_formula": {
            "description": "Priority Score = (ARR_Weight * 0.40) + (Strategic_Alignment * 0.30) + (Account_Health * 0.20) + (Effort_Inverse * 0.10)",
            "components": [
                {"name": "ARR Weight", "weight": 0.40, "calculation": "Sum of ARR from requesting accounts / Max possible ARR"},
                {"name": "Strategic Alignment", "weight": 0.30, "calculation": "high=1.0, medium=0.6, low=0.2"},
                {"name": "Account Health", "weight": 0.20, "calculation": "Average health score of requesting accounts / 100"},
                {"name": "Effort Inverse", "weight": 0.10, "calculation": "S=1.0, M=0.7, L=0.4, XL=0.2"},
            ],
        },
        "decision_gates": [
            {"gate": "Quick Win", "criteria": "Priority > 0.7 AND Effort <= M", "action": "Ship immediately"},
            {"gate": "Strategic Bet", "criteria": "Priority > 0.6 AND Strategic = high", "action": "Resource & plan for quarter"},
            {"gate": "Deferred", "criteria": "Priority < 0.4 OR Effort = XL with low alignment", "action": "Park for later review"},
        ],
        "quarterly_planning": {
            "capacity_allocation": {"quick_wins": "20%", "strategic_bets": "60%", "tech_debt": "20%"},
            "review_cadence": "Monthly prioritization review, quarterly roadmap commit",
        },
    }