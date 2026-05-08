from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class BotPersona(BaseModel):
    bot_id: str = Field(..., description="Unique identifier for the bot persona")
    name: str = Field(..., description="Name of the bot persona")
    persona: str = Field(..., description="Description of the bot persona's characteristics and behavior")

class RouteResult(BaseModel):
    bot_id: str
    bot_name: str
    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0
    )

    matched: bool

class BotPost(BaseModel):
    bot_id: str 
    topic: str = Field(..., min_length=3, max_length=50)
    post_content: str = Field(..., max_length=200)

#TypedDict for GraphState to be used in the graph database interactions
class GraphState(TypedDict):
    bot_id: str
    persona: str
    topic: str
    search_query: str
    search_results: str
    post_content: str

class DebateContext(BaseModel):
    parent_post: str

    comment_history: list[str]

    latest_human_reply: str