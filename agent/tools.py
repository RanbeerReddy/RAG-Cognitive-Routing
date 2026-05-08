from dotenv import load_dotenv

from langchain_tavily import TavilySearch
from langchain.tools import tool
from agent.config import TAVILY_API_KEY

import os



search_tool = TavilySearch(
    max_results=3,
    topic="general"
)


@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for recent information
    using Tavily Search API.
    """

    try:

        results = search_tool.invoke(query)

        return str(results)

    except Exception as error:

        return f"Search tool error: {str(error)}"


if __name__ == "__main__":

    queries = [

        "latest OpenAI news",

        "bitcoin ETF adoption",

        "AI replacing software engineers",

        "AI surveillance privacy concerns"
    ]

    print("\n" + "=" * 60)
    print("TAVILY SEARCH TOOL TESTING")
    print("=" * 60)

    for query in queries:

        print(f"\nQuery: {query}")

        result = web_search_tool.invoke(query)

        print("\nSearch Results:\n")
        print(result)

        print("\n" + "-" * 60)