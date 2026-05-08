

from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

from agent.schemas import GraphState, BotPost
from agent.tools import web_search_tool

from prompts.router_prompt import ROUTER_PROMPT
from prompts.drafting_prompt import DRAFTING_PROMPT

from dotenv import load_dotenv

import os


load_dotenv()


llm = ChatOllama(
    model=os.getenv("MODEL_NAME", "llama3"),
    temperature=0.7
)


structured_llm = llm.with_structured_output(BotPost)


# Decide what topic the bot wants to post about

def decide_search_node(state: GraphState) -> GraphState:

    persona = state["persona"]
    bot_name = state["bot_name"]

    prompt = ROUTER_PROMPT.format(
        persona=persona,
        bot_name=bot_name
    )

    response = llm.invoke(prompt)

    response_text = response.content.strip()

    topic = "AI Trends"
    search_query = "latest artificial intelligence news"

    lines = response_text.split("\n")

    for line in lines:

        if line.lower().startswith("topic:"):
            topic = line.split(":", 1)[1].strip()

        elif line.lower().startswith("search query:"):
            search_query = line.split(":", 1)[1].strip()

    return {
        **state,
        "topic": topic,
        "search_query": search_query
    }


# Search the web for recent context

def web_search_node(state: GraphState) -> GraphState:

    search_query = state["search_query"]

    raw_results = web_search_tool.invoke(search_query)

    formatted_results = []

    if isinstance(raw_results, dict):

        results = raw_results.get("results", [])

        for result in results:

            title = result.get("title", "")

            snippet = result.get("content", "")[:300]

            formatted_results.append(
                f"Title: {title}\n"
                f"Snippet: {snippet}"
            )

    clean_context = "\n\n".join(formatted_results)

    return {
        **state,
        "search_results": clean_context
    }

#response
# Generate final social media post

def draft_post_node(state: GraphState) -> GraphState:

    persona = state["persona"]
    bot_name = state["bot_name"]
    topic = state["topic"]
    search_results = state["search_results"]
    bot_id = state["bot_id"]

    prompt = DRAFTING_PROMPT.format(
        persona=persona,
        bot_name=bot_name,
        topic=topic,
        search_results=search_results
    )

    try:

        response = structured_llm.invoke(prompt)

    except Exception as error:

        response = BotPost(
            bot_id=bot_id,
            topic=topic,
            post_content="AI systems are rapidly reshaping society."
        )

    final_post = BotPost(
        bot_id=bot_id,
        topic=response.topic,
        post_content=response.post_content
    )

    return {
        **state,
        "post_content": final_post
    }


# Build LangGraph workflow

def build_graph():

    graph_builder = StateGraph(GraphState)

    graph_builder.add_node(
        "decide_search",
        decide_search_node
    )

    graph_builder.add_node(
        "web_search",
        web_search_node
    )

    graph_builder.add_node(
        "draft_post",
        draft_post_node
    )

    graph_builder.set_entry_point("decide_search")

    graph_builder.add_edge(
        "decide_search",
        "web_search"
    )

    graph_builder.add_edge(
        "web_search",
        "draft_post"
    )

    graph_builder.add_edge(
        "draft_post",
        END
    )

    return graph_builder.compile()


graph = build_graph()


if __name__ == "__main__":

    initial_state = {
        "bot_id": "bot_a",
        "bot_name": "Tech Maximalist",
        "persona": (
            "I strongly support artificial intelligence, automation, "
            "OpenAI, software innovation, coding assistants, robotics, "
            "crypto, Elon Musk, AGI, startups, and technological progress. "
            "I believe AI will replace many traditional jobs and improve society."
        ),
        "topic": None,
        "search_query": None,
        "search_results": None,
        "post_content": None
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 70)
    print("LANGGRAPH EXECUTION RESULT")
    print("=" * 70)

    print(f"\nBot ID: {result['bot_id']}")

    print(f"\nTopic:\n{result['topic']}")

    print(f"\nSearch Query:\n{result['search_query']}")

    print(f"\nSearch Results:\n{result['search_results'][:1000]}")

    final_post = result["post_content"]

    print(final_post.model_dump_json(indent=2))
