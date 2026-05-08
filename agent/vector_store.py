from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from agent.schemas import BotPersona, RouteResult


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

BOT_PERSONAS = [

   BotPersona(
        bot_id="bot_a",
        name="Tech Maximalist",
        persona=(
            "I strongly support artificial intelligence, automation, "
            "OpenAI, software innovation, coding assistants, robotics, "
            "crypto, Elon Musk, AGI, startups, and technological progress. "
            "I believe AI will replace many traditional jobs and improve society."
        )
    ),

    BotPersona(
        bot_id="bot_b",
        name="Doomer / Skeptic",
        persona=(
            "I believe AI automation, tech monopolies, social media, "
            "and billionaires are harming society. I criticize OpenAI, "
            "surveillance capitalism, job replacement, privacy violations, "
            "and corporate control over technology."
        )
    ),

    BotPersona(
        bot_id="bot_c",
        name="Finance Bro",
        persona=(
            "I care about financial markets, investing, trading algorithms, "
            "stocks, interest rates, AI startups, crypto profits, venture capital, "
            "and maximizing ROI from technology and automation."
        )
    )
]

#create embeddings
def embed_text(text: str) -> np.ndarray:
    """
    Convert text into embedding vector.

    Args:
        text (str): Input text.

    Returns:
        np.ndarray: Embedding vector.
    """

    embedding = embedding_model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    return embedding.astype(np.float32)


persona_ids = []
persona_objects = []
persona_embeddings = []



for bot in BOT_PERSONAS:

    embedding = embed_text(bot.persona)

    persona_ids.append(bot.bot_id)
    persona_objects.append(bot)
    persona_embeddings.append(embedding)


# Convert list -> numpy matrix
persona_embeddings = np.array(persona_embeddings)


# FAISS IndexFlatIP performs inner product search.
# If vectors are normalized first,
# inner product becomes cosine similarity.
# faiss.normalize_L2(persona_embeddings)


# Create FAISS index and add persona embeddings
embedding_dimension = persona_embeddings.shape[1]
index = faiss.IndexFlatIP(embedding_dimension)

index.add(persona_embeddings)

# Search Function
def search_similar_personas(
    query: str,
    top_k: int = 3
) -> list[RouteResult]:

    """
    Search for semantically similar personas.

    Args:
        query (str): Incoming post content
        top_k (int): Number of nearest neighbors

    Returns:
        list[RouteResult]
    """

    # Generate query embedding
    query_embedding = embed_text(query)

    # FAISS expects 2D array
    query_embedding = np.array([query_embedding])

    # Normalize query embedding
    faiss.normalize_L2(query_embedding)

    # Search index
    similarity_scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(
        similarity_scores[0],
        indices[0]
    ):

        matched_bot = persona_objects[idx]

        result = RouteResult(
            bot_id=matched_bot.bot_id,
            bot_name=matched_bot.name,
            similarity_score=round(float(score), 4),
            matched=True
        )

        results.append(result)

    return results

if __name__ == "__main__":

    incoming_post = (
        "OpenAI released a new coding model "
        "that may replace junior developers."
    )

    results = search_similar_personas(incoming_post)

    print("\n" + "=" * 60)
    print("INCOMING POST")
    print("=" * 60)
    print(incoming_post)

    print("\n" + "=" * 60)
    print("SIMILARITY RESULTS")
    print("=" * 60)

    for result in results:

        print(f"\nBot ID: {result.bot_id}")
        print(f"Bot Name: {result.bot_name}")
        print(f"Similarity Score: {result.similarity_score}")