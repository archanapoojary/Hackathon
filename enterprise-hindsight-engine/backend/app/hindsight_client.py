"""
Hindsight SDK Wrapper for persistent memory operations.
Provides retain, recall, and reflect capabilities for account-level context.
"""

import os
import json
from typing import Any, Optional
from dataclasses import dataclass

import httpx

from app.config import settings


@dataclass
class MemoryEntry:
    """Represents a memory entry in Hindsight."""
    entity_id: str
    content: str
    metadata: dict[str, Any]


@dataclass
class RecallResult:
    """Result from recalling context from Hindsight."""
    context: str
    memories: list[MemoryEntry]
    confidence: float


class HindsightClient:
    """
    Client for interacting with Hindsight memory API.
    Handles retain, recall, and reflect operations for account-level context.
    """

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_url = api_url or settings.hindsight_api_url
        self.api_key = api_key or settings.hindsight_api_key
        self.timeout = httpx.Timeout(30.0, connect=10.0)

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        } if self.api_key else {"Content-Type": "application/json"}

        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.api_url,
                headers=self.headers,
                timeout=self.timeout,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def retain_memory(
        self,
        entity_id: str,
        content: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Insert interaction context into Hindsight memory.

        Args:
            entity_id: Unique identifier for the entity (account_id, deal_id, etc.)
            content: The text content to store
            metadata: Additional structured metadata (stage, persona, timestamps, etc.)

        Returns:
            Response from Hindsight API
        """
        payload = {
            "entity_id": entity_id,
            "content": content,
            "metadata": metadata or {},
        }

        if not self.api_key:
            # Simulation mode for development
            return {
                "status": "success",
                "message": "Memory retained successfully (simulation mode)",
                "entity_id": entity_id,
            }

        try:
            response = await self.client.post("/retain", json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"status": "error", "message": f"Failed to retain memory: {str(e)}"}

    async def recall_context(
        self,
        entity_id: str,
        query: str,
        limit: int = 10,
        filters: Optional[dict[str, Any]] = None,
    ) -> RecallResult:
        """
        Recall historical context and objection graphs from Hindsight.

        Args:
            entity_id: Unique identifier for the entity
            query: Natural language query for retrieval
            limit: Maximum number of memories to retrieve
            filters: Optional metadata filters

        Returns:
            RecallResult with context and memories
        """
        payload = {
            "entity_id": entity_id,
            "query": query,
            "limit": limit,
            "filters": filters or {},
        }

        if not self.api_key:
            # Simulation mode for development
            simulated_context = self._get_simulated_context(entity_id, query)
            return RecallResult(
                context=simulated_context,
                memories=[],
                confidence=0.85,
            )

        try:
            response = await self.client.post("/recall", json=payload)
            response.raise_for_status()
            data = response.json()

            memories = [
                MemoryEntry(
                    entity_id=m.get("entity_id", entity_id),
                    content=m.get("content", ""),
                    metadata=m.get("metadata", {}),
                )
                for m in data.get("memories", [])
            ]

            return RecallResult(
                context=data.get("context", ""),
                memories=memories,
                confidence=data.get("confidence", 0.0),
            )
        except httpx.HTTPError as e:
            return RecallResult(
                context=f"Error recalling context: {str(e)}",
                memories=[],
                confidence=0.0,
            )

    async def reflect(
        self,
        entity_id: str,
        reflection_type: str = "objection_evolution",
        time_window_days: int = 90,
    ) -> dict[str, Any]:
        """
        Perform reflection/analysis on accumulated memories.

        Args:
            entity_id: Unique identifier for the entity
            reflection_type: Type of reflection (objection_evolution, stakeholder_sentiment, deal_momentum)
            time_window_days: Lookback window in days

        Returns:
            Reflection analysis results
        """
        payload = {
            "entity_id": entity_id,
            "reflection_type": reflection_type,
            "time_window_days": time_window_days,
        }

        if not self.api_key:
            return self._get_simulated_reflection(entity_id, reflection_type)

        try:
            response = await self.client.post("/reflect", json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"status": "error", "message": f"Reflection failed: {str(e)}"}

    def _get_simulated_context(self, entity_id: str, query: str) -> str:
        """Generate simulated context for development."""
        contexts = {
            "objections": (
                "Historical Objection Timeline:\n"
                "- Call 1 (Discovery): Champion raised 'budget constraints for Q3'\n"
                "- Call 3 (Technical): CTO questioned 'API latency at scale'\n"
                "- Call 5 (Negotiation): Procurement demanded '30% discount & net-60 terms'\n"
                "- Call 7 (Security Review): CISO required 'SOC2 Type II + penetration test results'\n"
                "\nWinning Patterns:\n"
                "- Technical objections resolved with architecture deep-dive + POC\n"
                "- Pricing objections overcome with ROI calculator + multi-year discount\n"
                "- Security concerns addressed by sharing audit reports proactively"
            ),
            "stakeholders": (
                "Stakeholder Map:\n"
                "- Sarah Jenkins (VP Engineering) - CHAMPION: Strong advocate, controls technical eval\n"
                "- Michael Chen (CTO) - DECISION MAKER: Concerned about latency & vendor lock-in\n"
                "- Lisa Park (CFO) - ECONOMIC BUYER: Needs clear ROI, prefers multi-year deals\n"
                "- James Wilson (Procurement) - GATEKEEPER: Requires 3 quotes, standard terms\n"
                "- Amanda Foster (CISO) - BLOCKER: Strict security requirements, slow to approve\n"
            ),
            "competitors": (
                "Competitive Intelligence:\n"
                "- Competitor A: Positioned on 'lower price' but lacks enterprise security\n"
                "- Competitor B: Strong on 'AI features' but implementation takes 6+ months\n"
                "- Our Win Themes: Faster deployment (4 weeks), superior security posture, dedicated CSM\n"
                "- Landmines: Avoid feature comparison on AI; pivot to time-to-value & security"
            ),
        }

        query_lower = query.lower()
        if any(k in query_lower for k in ["objection", "objections", "concern", "blocker"]):
            return contexts["objections"]
        elif any(k in query_lower for k in ["stakeholder", "persona", "buyer", "champion", "decision"]):
            return contexts["stakeholders"]
        elif any(k in query_lower for k in ["competitor", "competition", "alternative", "vs"]):
            return contexts["competitors"]
        else:
            return (
                f"Account {entity_id} - General Context:\n"
                f"Query: {query}\n"
                f"12 interactions synchronized over 90 days.\n"
                f"Current stage: Technical Validation.\n"
                f"Key risk: Security review timeline.\n"
                f"Key opportunity: Champion has budget authority for pilot."
            )

    def _get_simulated_reflection(self, entity_id: str, reflection_type: str) -> dict[str, Any]:
        """Generate simulated reflection for development."""
        reflections = {
            "objection_evolution": {
                "entity_id": entity_id,
                "reflection_type": "objection_evolution",
                "summary": "Objections have evolved from budget → technical → security → procurement.",
                "stages": [
                    {"stage": "Discovery", "primary_objection": "Budget timing", "resolved": True},
                    {"stage": "Technical", "primary_objection": "API latency at scale", "resolved": True, "resolution": "POC demonstrated <50ms p99"},
                    {"stage": "Security", "primary_objection": "SOC2 Type II required", "resolved": False, "eta_days": 14},
                    {"stage": "Procurement", "primary_objection": "Contract terms & discount", "resolved": False},
                ],
                "recommended_actions": [
                    "Accelerate SOC2 Type II audit sharing",
                    "Prepare multi-year discount structure",
                    "Engage CFO with ROI model this week",
                ],
            },
            "stakeholder_sentiment": {
                "entity_id": entity_id,
                "reflection_type": "stakeholder_sentiment",
                "sentiment_trend": "improving",
                "stakeholders": {
                    "Sarah Jenkins (VP Eng)": {"sentiment": 0.9, "influence": "high", "trend": "stable"},
                    "Michael Chen (CTO)": {"sentiment": 0.6, "influence": "high", "trend": "improving"},
                    "Lisa Park (CFO)": {"sentiment": 0.4, "influence": "high", "trend": "stable"},
                    "James Wilson (Procurement)": {"sentiment": 0.3, "influence": "medium", "trend": "declining"},
                    "Amanda Foster (CISO)": {"sentiment": 0.2, "influence": "high", "trend": "stable"},
                },
                "risk_factors": ["CISO not yet engaged", "Procurement pushing competitor"],
                "action_items": ["Schedule CISO 1:1", "CFO ROI workshop"],
            },
            "deal_momentum": {
                "entity_id": entity_id,
                "reflection_type": "deal_momentum",
                "momentum_score": 0.72,
                "trend": "positive",
                "velocity_indicators": {
                    "meeting_frequency": "weekly",
                    "stakeholder_engagement": "increasing",
                    "technical_milestones": "on_track",
                    "contract_progress": "drafting",
                },
                "risk_score": 0.35,
                "close_probability": 0.68,
                "recommended_next_steps": [
                    "Finalize security questionnaire responses",
                    "Present executive business case to CFO",
                    "Negotiate contract redlines with Procurement",
                ],
            },
        }

        return reflections.get(reflection_type, {"status": "unknown_reflection_type"})


# Global client instance
hindsight_client = HindsightClient()