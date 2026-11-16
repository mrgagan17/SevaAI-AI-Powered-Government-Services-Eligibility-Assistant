from typing import Dict, Any, List, Optional
import re
from backend.models.database_models import UserProfile
from backend.models.schemas import EligibilityResult, EligibilityCriterion
from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import ELIGIBILITY_EVALUATION_PROMPT
from backend.utils.logging_config import logger

class EligibilityService:
    """Evaluates citizen eligibility against indexed government requirements."""

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.ollama = ollama_client or OllamaClient()

    def evaluate_eligibility(
        self,
        profile: Optional[UserProfile],
        question: str,
        context: str,
        chunks: List[Dict[str, Any]]
    ) -> EligibilityResult:
        """
        Evaluate user eligibility against retrieved document context and profile.
        Returns EligibilityResult with breakdown of criteria.
        """
        if not profile:
            return EligibilityResult(
                status="UNKNOWN",
                summary="User profile is not configured. Please fill in your profile for personalized eligibility matching.",
                criteria=[],
                disclaimer="SevaAI guidance only. Verify official notification."
            )

        if not chunks or "No relevant official documents found" in context:
            return EligibilityResult(
                status="UNKNOWN",
                summary="Insufficient government document context available to evaluate eligibility requirements.",
                criteria=[],
                disclaimer="SevaAI guidance only. Verify official notification."
            )

        criteria_list: List[EligibilityCriterion] = []
        full_text = " ".join([c.get("text", "") for c in chunks]).lower()

        # Rule-based evaluation helpers for robust, instant evaluation
        match_count = 0
        mismatch_count = 0
        unknown_count = 0

        # 1. Age Evaluation
        user_age = profile.age
        age_status = "UNKNOWN"
        age_note = "Age requirement not explicitly found in context."
        if user_age is not None:
            # Check for age bounds in text e.g. "age 18 to 35", "max 30 years", "above 18 years"
            min_age_match = re.search(r'(?:minimum|min|above|at least)\s+(\d{2})\s*(?:years|yrs)?', full_text)
            max_age_match = re.search(r'(?:maximum|max|up to|not exceeding)\s+(\d{2})\s*(?:years|yrs)?', full_text)
            range_match = re.search(r'(?:age|aged)\s*(?:between)?\s*(\d{2})\s*(?:to|-|and)\s*(\d{2})', full_text)

            min_age = int(range_match.group(1)) if range_match else (int(min_age_match.group(1)) if min_age_match else None)
            max_age = int(range_match.group(2)) if range_match else (int(max_age_match.group(1)) if max_age_match else None)

            if min_age is not None or max_age is not None:
                satisfied = True
                if min_age is not None and user_age < min_age:
                    satisfied = False
                if max_age is not None and user_age > max_age:
                    satisfied = False

                if satisfied:
                    age_status = "MATCH"
                    age_note = f"Your age ({user_age}) satisfies the listed range."
                else:
                    age_status = "NOT_MATCHED"
                    age_note = f"Your age ({user_age}) does not fit the required criteria ({min_age or 0}-{max_age or 'N/A'})."
            else:
                age_note = f"Your age is {user_age}. Specific age limit not found in retrieved snippet."

        criteria_list.append(EligibilityCriterion(
            criterion="Age Requirement",
            status=age_status,
            user_value=str(user_age) if user_age else "Not specified",
            required_value="See source",
            note=age_note
        ))

        # 2. Education Evaluation
        user_edu = profile.education or "Unknown"
        edu_status = "UNKNOWN"
        edu_note = "Educational requirement details not detected."
        if user_edu and user_edu != "Unknown":
            if any(term in full_text for term in ["qualification", "degree", "graduate", "diploma", "sslc", "10th", "12th", "postgraduate", "master"]):
                # Simple keyword matching check
                if user_edu.lower() in full_text:
                    edu_status = "MATCH"
                    edu_note = f"Requirement for '{user_edu}' appears satisfied based on document text."
                else:
                    edu_status = "PARTIAL_MATCH"
                    edu_note = f"Educational qualification ({user_edu}) mentioned; verify exact specialization."

        criteria_list.append(EligibilityCriterion(
            criterion="Educational Qualification",
            status=edu_status,
            user_value=user_edu,
            required_value="See document details",
            note=edu_note
        ))

        # 3. Income Evaluation
        user_income = profile.annual_income
        inc_status = "UNKNOWN"
        inc_note = "Income threshold not found in the available source."
        if user_income is not None:
            inc_match = re.search(r'(?:income|family income)\s*(?:less than|below|not exceeding|up to|max)?\s*(?:rs\.?|inr|₹)?\s*([\d,]+)', full_text)
            if inc_match:
                limit_str = inc_match.group(1).replace(',', '')
                if limit_str.isdigit():
                    limit = float(limit_str)
                    if user_income <= limit:
                        inc_status = "MATCH"
                        inc_note = f"Annual income (₹{user_income:,.0f}) is below limit (₹{limit:,.0f})."
                    else:
                        inc_status = "NOT_MATCHED"
                        inc_note = f"Annual income (₹{user_income:,.0f}) exceeds listed limit (₹{limit:,.0f})."

        criteria_list.append(EligibilityCriterion(
            criterion="Income Limit",
            status=inc_status,
            user_value=f"₹{user_income:,.0f}" if user_income is not None else "Not specified",
            required_value="See document details",
            note=inc_note
        ))

        # 4. Category Evaluation
        user_cat = profile.category or "General"
        cat_status = "MATCH" if "category" in full_text or "reservation" in full_text else "UNKNOWN"
        criteria_list.append(EligibilityCriterion(
            criterion="Social Category / Reservation",
            status=cat_status,
            user_value=user_cat,
            required_value="Applicable category",
            note=f"Your listed category is {user_cat}."
        ))

        # Aggregate overall status
        statuses = [c.status for c in criteria_list]
        if "NOT_MATCHED" in statuses:
            overall_status = "NOT_MATCHED"
            summary_text = "Based on available documents, you do not appear to meet all listed eligibility requirements."
        elif "MATCH" in statuses and "NOT_MATCHED" not in statuses:
            if "UNKNOWN" in statuses or "PARTIAL_MATCH" in statuses:
                overall_status = "PARTIAL_MATCH"
                summary_text = "Based on the available document and your profile information, you appear to meet some conditions, but some requirements could not be verified."
            else:
                overall_status = "MATCH"
                summary_text = "Based on the available document and your profile information, you appear to meet the listed conditions."
        else:
            overall_status = "UNKNOWN"
            summary_text = "Eligibility requirements could not be conclusively determined from the available document context."

        return EligibilityResult(
            status=overall_status,
            summary=summary_text,
            criteria=criteria_list,
            disclaimer="SevaAI guidance only. Information should be verified with the official government source before taking action."
        )
