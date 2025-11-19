import logging
from typing import Any

from langchain_core.runnables import Runnable
from langchain_core.messages import SystemMessage, HumanMessage

from ..state.ai_news_state import AINewsState
from newsbot.core.config import SessionConfig

logger = logging.getLogger(__name__)


class NewsSummarizeNode:
    """Node for summarizing fetched news articles using LLM."""

    def __init__(self, llm: Runnable, session_config: SessionConfig) -> None:
        self.session_config = session_config
        self.llm = llm

    def summarize(self, state: AINewsState) -> dict:
        """
        Summarize the fetched news using an LLM.

        Args:
            state: The state containing fetched news results

        Returns:
            Dict containing the generated summary
        """
        logger.info("Starting news summarization")

        fetched_results = state.get("fetch_results", [])
        time_frame = self.session_config.selected_ai_news_frame or "Unknown"

        # Validate input
        if not fetched_results:
            logger.warning("No fetched results available for summarization")
            return {"summary": f"No AI news articles available for {time_frame}."}

        # Create comprehensive system prompt for news summarization
        system_prompt = f"""
        You are an expert AI news analyst. Given a collection of fetched AI/tech news items (list of dicts) for the timeframe: {time_frame}, produce a high‑quality, concise markdown report.

        GOALS:
        1. Distill each article into core points (facts, impacts, novelty) without duplication.
        2. Highlight trends that span multiple articles (e.g., funding, regulation, safety, product releases, research breakthroughs).
        3. Normalize dates to ISO (YYYY-MM-DD) and convert times to UTC if present.
        4. Remove boilerplate, repeated promotional sentences, and duplicate content blocks.
        5. If multiple articles reference same event (same or similar title / URL host + overlapping content), merge them, noting sources.
        6. Prefer objective tone; no hype words (e.g., "revolutionary", "game-changing") unless direct quotes.

        OUTPUT MARKDOWN STRUCTURE (strict):
        # {time_frame} AI News Summary
        ## Snapshot
        - Total Articles: <number>
        - Distinct Events: <number>
        - Key Themes: <comma-separated short phrases>

        ## Themes
        For each major theme, use:
        ### <Theme Name>
        - Summary: <2-3 sentence synthesis>
        - Notable Items:
          - <Title> — <One sentence impact> (Source: <domain>, Date: <YYYY-MM-DD>)

        ## Articles
        For each merged/distinct article/event:
        ### <Concise Title>
        - Date: <YYYY-MM-DD>
        - Source: <domain>
        - Category: one of [Research, Product, Funding, Regulation, Security, Ethics, Other]
        - Key Points:
          - <bullet fact>
          - <bullet fact>
        - Impact: <short statement of potential significance>
        - Links: <primary URL> [and any merged additional sources]

        ## Metrics & Signals
        - Research Breakthroughs: <count>
        - New Products/Features: <count>
        - Funding / M&A: <count>
        - Regulatory / Policy: <count>
        - Safety / Security Incidents: <count>

        ## Trend Commentary
        Provide 3-5 bullets forecasting near-term implications.

        ## Raw Sources
        A markdown table with columns: Date | Title | Domain | URL

        RULES:
        - If content field is extremely long, summarize; do not echo large blocks.
        - If raw_content is 'None' ignore it.
        - Preserve factual accuracy; if uncertain, omit rather than speculate.
        - Never fabricate URLs or dates.
        - If fetched_results is empty or None, return a markdown section: "No articles available for timeframe {time_frame}."
        - Keep total length under ~1200 words.

        VALIDATE BEFORE RETURN:
        - Ensure required top-level headers exist.
        - Ensure no placeholder tokens like <number> remain; replace them.
        - Ensure bullet lists have at least one item or omit the section gracefully.

        Return ONLY markdown, no surrounding commentary.
        """
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(
                    content=f"time_frame: {time_frame}\nfetched_results: {fetched_results}"
                ),
            ]

            logger.info(f"Summarizing {len(fetched_results)} articles for {time_frame}")
            response = self.llm.invoke(messages)

            logger.info("Successfully generated news summary")
            return {"summary": response.content}

        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            error_summary = f"# {time_frame} AI News Summary\n\nError: Unable to generate summary due to: {str(e)}"
            return {"summary": error_summary}
