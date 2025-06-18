import asyncio
import httpx
from typing import Callable, List, Optional, Tuple, Dict
from providers import get_model, trim_prompt
from prompt import system_prompt
from text_splitter import RecursiveCharacterTextSplitter
from config import FIRECRAWL_KEY, FIRECRAWL_BASE_URL, FIRECRAWL_CONCURRENCY


async def fetch_serp_results(query: str) -> List[Dict]:
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            FIRECRAWL_BASE_URL or "https://api.firecrawl.dev/v1/search",
            headers={"Authorization": f"Bearer {FIRECRAWL_KEY}"},
            json={"query": query, "limit": 5, "scrapeOptions": {"formats": ["markdown"]}},
        )
        response.raise_for_status()
        return response.json()["data"]


async def generate_serp_queries(prompt: str, learnings: Optional[List[str]] = None, num_queries: int = 3) -> List[Dict]:
    model = get_model()

    previous_learnings = ""
    if learnings:
        previous_learnings = "Previous learnings:\n" + "\n".join(learnings)

    user_prompt = f"""Given the user prompt below, generate up to {num_queries} unique SERP queries.
<query>{prompt}</query>

{previous_learnings}
"""

    messages = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": user_prompt},
    ]
    response = model.generate(messages)
    lines = [line.strip("- ").strip() for line in response.split("\n") if line.strip()]
    return [{"query": q, "researchGoal": ""} for q in lines[:num_queries]]


async def process_serp(query: str, results: List[Dict]) -> Tuple[List[str], List[str]]:
    contents = [trim_prompt(r.get("markdown", ""), 25000) for r in results if r.get("markdown")]
    combined_content = "\n".join([f"<content>{c}</content>" for c in contents])

    model = get_model()
    prompt = f"""From the following SERP results, extract up to 3 key learnings and 3 follow-up questions to explore the topic further.

<query>{query}</query>
{combined_content}
"""
    messages = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": trim_prompt(prompt)},
    ]
    response = model.generate(messages)

    learnings = []
    questions = []
    for line in response.split("\n"):
        if "?" in line:
            questions.append(line.strip("- ").strip())
        elif line.strip():
            learnings.append(line.strip("- ").strip())
    return learnings[:3], questions[:3]


async def deep_research(
    query: str,
    depth: int,
    breadth: int,
    learnings: Optional[List[str]] = None,
    visited_urls: Optional[List[str]] = None,
    on_progress: Optional[Callable[[Dict], None]] = None,
) -> Dict[str, List[str]]:
    learnings = learnings or []
    visited_urls = visited_urls or []
    serp_queries = await generate_serp_queries(query, learnings, num_queries=breadth)

    semaphore = asyncio.Semaphore(FIRECRAWL_CONCURRENCY)
    all_learnings = list(learnings)
    all_urls = list(visited_urls)

    async def handle_query(q_obj: Dict):
        q = q_obj["query"]
        async with semaphore:
            try:
                results = await fetch_serp_results(q)
                urls = [r["url"] for r in results if r.get("url")]
                new_learnings, followups = await process_serp(q, results)

                all_learnings.extend(new_learnings)
                all_urls.extend(urls)

                if depth > 1:
                    followup_query = f"{q}\n" + "\n".join(followups)
                    result = await deep_research(
                        query=followup_query,
                        depth=depth - 1,
                        breadth=max(1, breadth // 2),
                        learnings=all_learnings,
                        visited_urls=all_urls,
                        on_progress=on_progress,
                    )
                    all_learnings.extend(result["learnings"])
                    all_urls.extend(result["visited_urls"])
            except Exception as e:
                print(f"[error] {q}: {e}")

    await asyncio.gather(*[handle_query(q) for q in serp_queries])

    return {
        "learnings": list(set(all_learnings)),
        "visited_urls": list(set(all_urls)),
    }
