import logging
from pydantic import BaseModel
from pathlib import Path

from pydantic import BaseModel

from ..state.ai_news_state import AINewsState
from newsbot.core.config import SessionConfig

logger = logging.getLogger(__name__)


class SaveNewsNode(BaseModel):
    """Node for saving AI news summary to markdown files."""
    session_config: SessionConfig

    def save_result(self, state: AINewsState) -> dict:
        """Saves the generated summary to markdown files."""
        logger.info("Starting save operation for news summary")

        # Get summary and time frame
        summary = state.get("summary", "")
        time_frame = self.session_config.selected_ai_news_frame or "Unknown"
        
        # Validate summary content
        if not summary or summary.strip() == "":
            logger.warning("No summary content available to save")
            return {**state}
            
        # Create file path
        file_name = f"{time_frame}_summary.md"
        file_path = Path("./AI_News") / file_name
        
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write summary to file
            file_path.write_text(summary, encoding='utf-8')
            
            logger.info(f"Successfully saved AI news summary to {file_path}")
            return {**state}
            
        except Exception as e:
            logger.error(f"Failed to save summary to {file_path}: {e}")
            # Continue pipeline even if save fails
            return {**state}
