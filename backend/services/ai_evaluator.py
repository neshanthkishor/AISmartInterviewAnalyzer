from typing import Dict, List


class AIAnswerEvaluator:
    """
    Local AI-style interview answer evaluator.

    This version does not require an external API key.
    It evaluates answers using structured scoring rules so
    the project can run completely on a local machine.
    """

    def __init__(self):
        self.minimum_answer_length = 20

    def evaluate(
        self,
        question: str,
        answer: str,
        interview_type: str = "Technical",
        role: str = "Software Developer"
    ) -> Dict:

        question = (question or "").strip()
        answer = (answer or "").strip()

        if not answer:
            return self._empty_result()

        words = answer.split()
        word_count = len(words)

        # --------------------------------------------------
        # 1. ANSWER QUALITY
        # --------------------------------------------------

        if word_count < 10:
            quality_score = 35
        elif word_count < 25:
            quality_score = 55
        elif word_count < 50:
            quality_score = 72
        elif word_count < 100:
            quality_score = 84
        else:
            quality_score = 90

        # --------------------------------------------------
        # 2. TECHNICAL KNOWLEDGE
        # --------------------------------------------------

        technical_keywords = [
            "algorithm",
            "data structure",
            "database",
            "api",
            "python",
            "java",
            "javascript",
            "sql",
            "testing",
            "debug",
            "function",
            "class",
            "object",
            "backend",
            "frontend",
            "framework",
            "optimization",
            "performance",
            "security",
            "exception",
            "code",
            "system",
            "architecture"
        ]

        answer_lower = answer.lower()

        technical_hits = sum(
            1 for keyword in technical_keywords
            if keyword in answer_lower
        )

        technical_score = min(
            95,
            45 + technical_hits * 5
        )

        if interview_type.lower() in ["hr", "hr / behavioral", "behavioral"]:
            technical_score = min(100, technical_score + 5)

        # --------------------------------------------------
        # 3. COMMUNICATION
        # --------------------------------------------------

        communication_words = [
            "because",
            "therefore",
            "however",
            "first",
            "then",
            "finally",
            "for example",
            "also",
            "although",
            "while",
            "result"
        ]

        communication_hits = sum(
            1 for keyword in communication_words
            if keyword in answer_lower
        )

        communication_score = min(
            95,
            55 + communication_hits * 5
        )

        if word_count >= 40:
            communication_score += 3

        communication_score = min(100, communication_score)

        # --------------------------------------------------
        # 4. PROBLEM SOLVING
        # --------------------------------------------------

        problem_solving_words = [
            "approach",
            "analyze",
            "understand",
            "break",
            "step",
            "solution",
            "solve",
            "test",
            "improve",
            "efficient",
            "optimize",
            "debug",
            "identify",
            "implement"
        ]

        problem_hits = sum(
            1 for keyword in problem_solving_words
            if keyword in answer_lower
        )

        problem_solving_score = min(
            96,
            50 + problem_hits * 5
        )

        # --------------------------------------------------
        # 5. CONFIDENCE
        # --------------------------------------------------

        weak_phrases = [
            "i don't know",
            "not sure",
            "maybe",
            "i think",
            "probably",
            "i guess",
            "no idea"
        ]

        weak_hits = sum(
            1 for phrase in weak_phrases
            if phrase in answer_lower
        )

        confidence_score = 82 - (weak_hits * 12)

        if word_count >= 30:
            confidence_score += 5

        confidence_score = max(
            35,
            min(98, confidence_score)
        )

        # --------------------------------------------------
        # 6. STRUCTURE
        # --------------------------------------------------

        structure_score = 60

        if any(
            word in answer_lower
            for word in ["first", "second", "then", "finally"]
        ):
            structure_score += 15

        if word_count >= 35:
            structure_score += 10

        if "." in answer:
            structure_score += 5

        structure_score = min(95, structure_score)

        # --------------------------------------------------
        # 7. OVERALL SCORE
        # --------------------------------------------------

        overall_score = round(
            (
                technical_score * 0.30
                + communication_score * 0.20
                + problem_solving_score * 0.20
                + confidence_score * 0.15
                + structure_score * 0.15
            )
        )

        # --------------------------------------------------
        # 8. STRENGTHS
        # --------------------------------------------------

        strengths: List[str] = []

        if technical_score >= 75:
            strengths.append(
                "Good technical understanding"
            )

        if communication_score >= 75:
            strengths.append(
                "Clear communication"
            )

        if problem_solving_score >= 75:
            strengths.append(
                "Strong problem-solving approach"
            )

        if confidence_score >= 75:
            strengths.append(
                "Confident response style"
            )

        if structure_score >= 75:
            strengths.append(
                "Well-structured answer"
            )

        if not strengths:
            strengths.append(
                "Shows willingness to explain the approach"
            )

        # --------------------------------------------------
        # 9. IMPROVEMENT AREAS
        # --------------------------------------------------

        improvements: List[str] = []

        if technical_score < 70:
            improvements.append(
                "Include more role-specific technical concepts."
            )

        if communication_score < 70:
            improvements.append(
                "Explain your ideas with clearer sentences and examples."
            )

        if problem_solving_score < 70:
            improvements.append(
                "Describe your problem-solving steps more explicitly."
            )

        if confidence_score < 70:
            improvements.append(
                "Use more direct and confident language."
            )

        if structure_score < 70:
            improvements.append(
                "Structure the answer using a clear beginning, approach and result."
            )

        if word_count < 25:
            improvements.append(
                "Provide a more detailed answer instead of a very short response."
            )

        if not improvements:
            improvements.append(
                "Continue adding specific examples to make strong answers even better."
            )

        # --------------------------------------------------
        # 10. PERFORMANCE LEVEL
        # --------------------------------------------------

        if overall_score >= 85:
            performance = "Excellent"
        elif overall_score >= 75:
            performance = "Strong"
        elif overall_score >= 60:
            performance = "Good"
        elif overall_score >= 45:
            performance = "Needs Improvement"
        else:
            performance = "Weak"

        # --------------------------------------------------
        # 11. AI FEEDBACK
        # --------------------------------------------------

        feedback = self._generate_feedback(
            overall_score,
            performance,
            strengths,
            improvements
        )

        return {
            "success": True,
            "overall_score": overall_score,
            "performance": performance,

            "scores": {
                "technical_knowledge": technical_score,
                "communication": communication_score,
                "problem_solving": problem_solving_score,
                "confidence": confidence_score,
                "answer_structure": structure_score
            },

            "analysis": {
                "word_count": word_count,
                "technical_keyword_hits": technical_hits,
                "problem_solving_signals": problem_hits,
                "communication_signals": communication_hits
            },

            "strengths": strengths,
            "improvements": improvements,
            "feedback": feedback,

            "question": question,
            "role": role
        }

    # ------------------------------------------------------
    # EMPTY ANSWER
    # ------------------------------------------------------

    def _empty_result(self):

        return {
            "success": True,
            "overall_score": 0,
            "performance": "No Answer",

            "scores": {
                "technical_knowledge": 0,
                "communication": 0,
                "problem_solving": 0,
                "confidence": 0,
                "answer_structure": 0
            },

            "analysis": {
                "word_count": 0,
                "technical_keyword_hits": 0,
                "problem_solving_signals": 0,
                "communication_signals": 0
            },

            "strengths": [],
            "improvements": [
                "Please provide an answer to receive AI feedback."
            ],

            "feedback": (
                "No answer was detected. "
                "Provide a complete response so InterviewIQ "
                "can evaluate your performance."
            ),

            "question": "",
            "role": ""
        }

    # ------------------------------------------------------
    # FEEDBACK GENERATOR
    # ------------------------------------------------------

    def _generate_feedback(
        self,
        score,
        performance,
        strengths,
        improvements
    ):

        if score >= 85:
            opening = (
                "Excellent response. Your answer demonstrates "
                "strong interview readiness."
            )

        elif score >= 75:
            opening = (
                "Strong response. You demonstrated good "
                "understanding and a useful interview approach."
            )

        elif score >= 60:
            opening = (
                "Good attempt. Your response has a solid foundation, "
                "but there are areas that can be improved."
            )

        elif score >= 45:
            opening = (
                "Your answer shows some understanding, "
                "but it needs more depth and structure."
            )

        else:
            opening = (
                "This answer needs significant improvement. "
                "Try explaining your reasoning in more detail."
            )

        return (
            f"{opening} "
            f"Current performance level: {performance}. "
            f"Focus on the improvement areas identified by InterviewIQ "
            f"for your next response."
        )


# ----------------------------------------------------------
# SINGLETON INSTANCE
# ----------------------------------------------------------

ai_evaluator = AIAnswerEvaluator()