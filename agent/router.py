

from agent.vector_store import search_similar_personas
from agent.schemas import RouteResult

from rich.console import Console

 
# RICH CONSOLE


console = Console()


 
# ROUTER FUNCTION


def route_post_to_bots(
    post_content: str,
    threshold: float = 0.60
) -> list[RouteResult]:

    """
    Route incoming post to relevant bots
    using semantic similarity.

    Args:
        post_content (str):
            Incoming social media post

        threshold (float):
            Minimum cosine similarity threshold

    Returns:
        list[RouteResult]:
            Filtered matching bots
    """

    # Semantic similarity search
    similarity_results = search_similar_personas(
        query=post_content,
        top_k=3
    )

    matched_bots = []

    # Apply routing threshold
    for result in similarity_results:

        if result.similarity_score >= threshold:

            matched_bots.append(result)

    return matched_bots



# DISPLAY RESULTS


def display_routing_results(
    post_content: str,
    results: list[RouteResult]
):

    """
    Pretty print routing results.
    """

    console.print(
        "\n" + "=" * 70,
        style="bold cyan"
    )

    console.print(
        "INCOMING POST",
        style="bold green"
    )

    console.print(
        "=" * 70,
        style="bold cyan"
    )

    console.print(f"\n{post_content}")

    console.print(
        "\n" + "=" * 70,
        style="bold cyan"
    )

    console.print(
        "ROUTING RESULTS",
        style="bold green"
    )

    console.print(
        "=" * 70,
        style="bold cyan"
    )

    if not results:

        console.print(
            "\nNo matching bots found.",
            style="bold red"
        )

        return

    for result in results:

        console.print(
            f"\nBot ID: {result.bot_id}",
            style="bold yellow"
        )

        console.print(
            f"Bot Name: {result.bot_name}"
        )

        console.print(
            f"Similarity Score: {result.similarity_score}",
            style="bold magenta"
        )

        console.print(
            f"Matched: {result.matched}",
            style="bold green"
        )


#testing

if __name__ == "__main__":

    incoming_post = (
        "OpenAI released a powerful new AI model "
        "that may replace junior software engineers."
    )

    routed_bots = route_post_to_bots(
        post_content=incoming_post,
        threshold=0.60
    )

    display_routing_results(
        post_content=incoming_post,
        results=routed_bots
    )