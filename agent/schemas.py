

from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import TypedDict



# BOT PERSONA SCHEMA


class BotPersona(BaseModel):

    model_config = {
        "extra": "forbid"
    }

    bot_id: str = Field(
        ...,
        description="Unique identifier for the bot persona"
    )

    name: str = Field(
        ...,
        description="Name of the bot persona"
    )

    persona: str = Field(
        ...,
        description="Detailed description of the bot's ideology, personality, and behavior"
    )



# ROUTING RESULT SCHEMA


class RouteResult(BaseModel):

    model_config = {
        "extra": "forbid"
    }

    bot_id: str = Field(
        ...,
        description="Unique identifier of the matched bot"
    )

    bot_name: str = Field(
        ...,
        description="Name of the matched bot"
    )

    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Cosine similarity score between post and persona"
    )

    matched: bool = Field(
        ...,
        description="Whether the bot passed routing threshold"
    )



# STRUCTURED LLM OUTPUT SCHEMA


class BotPost(BaseModel):

    model_config = {
        "extra": "forbid"
    }

    bot_id: str = Field(
        ...,
        description="Bot generating the post"
    )

    topic: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Topic selected by the AI bot"
    )

    post_content: str = Field(
        ...,
        max_length=280,
        description="Generated social media post"
    )



# ROUTER DECISION SCHEMA


class RouterDecision(BaseModel):

    model_config = {
        "extra": "forbid"
    }

    topic: str = Field(
        min_length=3,
        max_length=50,
        description="Topic selected by the bot"
    )

    search_query: str = Field(
        min_length=5,
        max_length=100,
        description="Web search query for gathering context"
    )



# LANGGRAPH STATE


class GraphState(TypedDict):

    bot_id: str
    bot_name: str
    persona: str

    topic: Optional[str]
    search_query: Optional[str]
    search_results: Optional[str]

    post_content: Optional[BotPost]

 
# DEBATE MESSAGE SCHEMA


class DebateMessage(BaseModel):

    model_config = {
        "extra": "forbid"
    }

    speaker: str = Field(
        ...,
        description="Speaker in the debate thread"
    )

    content: str = Field(
        ...,
        description="Message content"
    )



# RAG DEBATE CONTEXT


class DebateContext(BaseModel):

    model_config = {
        "extra": "forbid"
    }

    parent_post: str = Field(
        ...,
        description="Original parent post"
    )

    comment_history: list[DebateMessage] = Field(
        ...,
        description="Conversation history in the thread"
    )

    latest_human_reply: str = Field(
        ...,
        description="Latest human reply requiring defense response"
    )