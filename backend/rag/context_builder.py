from typing import List, Dict, Any

class ContextBuilder:
    """Formatter to compile retrieved document chunks into clean structured prompt context."""

    @staticmethod
    def build_context(chunks: List[Dict[str, Any]], max_chars: int = 4000) -> str:
        """Format chunks into structured text blocks for LLM context."""
        if not chunks:
            return "No relevant official documents found."

        context_blocks = []
        total_len = 0

        for i, chunk in enumerate(chunks, 1):
            block = (
                f"--- SOURCE {i} ---\n"
                f"Document: {chunk.get('source', 'Unknown')}\n"
                f"Page: {chunk.get('page', 'N/A')}\n"
                f"Category: {chunk.get('category', 'General')}\n"
                f"Content:\n{chunk.get('text', '').strip()}\n"
            )
            
            if total_len + len(block) > max_chars and context_blocks:
                break

            context_blocks.append(block)
            total_len += len(block)

        return "\n".join(context_blocks)
