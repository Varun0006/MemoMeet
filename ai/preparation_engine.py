from ai.groq_service import GroqService
from ai.prompt_templates import PREPARATION_PROMPT
from models.memory import Memory
from models.action_item import ActionItem
from models.meeting_participant import MeetingParticipant


class PreparationEngine:
    def __init__(self):
        self.gemini = GroqService()

    def generate_report(self, participant, user_id, sections=None, limit=10):
        meeting_count = MeetingParticipant.query.filter_by(participant_id=participant.id).count()
        memories = Memory.query.filter_by(participant_id=participant.id, user_id=user_id).order_by(Memory.created_at.desc()).limit(limit).all()
        commitments = ActionItem.query.filter_by(participant_id=participant.id, user_id=user_id, status="Pending").all()

        memories_text = "\n".join(f"- [{m.memory_type}] {m.content}" for m in memories) if memories else "No memories recorded."
        commitments_text = "\n".join(f"- {c.task} (deadline: {c.deadline})" for c in commitments) if commitments else "No open commitments."

        if self.gemini.is_available():
            section_instructions = []
            if not sections or "relationship" in sections:
                section_instructions.append("1. Relationship Summary (briefly overview past interactions and history; do not discuss numerical relationship status, health scores, or ratings since they are deprecated)")
            if not sections or "memories" in sections:
                section_instructions.append("2. Key Memories to Review")
            if not sections or "commitments" in sections:
                section_instructions.append("3. Open Commitments")
                section_instructions.append("4. Important Concerns")
                section_instructions.append("5. Risks to Address")
            if not sections or "questions" in sections:
                section_instructions.append("6. Suggested Questions to Ask")
                section_instructions.append("7. Suggested Discussion Topics")

            sections_text = "\n".join(section_instructions)

            prompt = PREPARATION_PROMPT.format(
                participant_name=participant.name,
                meeting_count=meeting_count,
                memories=memories_text,
                commitments=commitments_text,
                sections_text=sections_text,
            )
            return self.gemini.generate(prompt)
        else:
            return self._generate_fallback(participant, meeting_count, memories, commitments, sections=sections)

    def _generate_fallback(self, participant, meeting_count, memories, commitments, sections=None):
        lines = [f"## Preparation Report for {participant.name}"]
        lines.append(f"**Meetings recorded:** {meeting_count}\n")
        if not sections or "relationship" in sections:
            lines.append("### Relationship Summary")
            lines.append("- Collaboration history is active.\n")
        if not sections or "memories" in sections:
            lines.append("### Key Memories to Review")
            if memories:
                for m in memories:
                    lines.append(f"- [{m.memory_type}] {m.content[:100]}")
            else:
                lines.append("- No memories recorded.")
            lines.append("")
        if not sections or "commitments" in sections:
            lines.append("### Open Commitments")
            if commitments:
                for c in commitments:
                    lines.append(f"- {c.task}")
            else:
                lines.append("- No open commitments.")
            lines.append("")
        if not sections or "questions" in sections:
            lines.append("### Suggested Questions to Ask")
            lines.append("1. How have things been since our last meeting?")
            lines.append("2. Any updates on the topics we discussed?\n")
        return "\n".join(lines)
