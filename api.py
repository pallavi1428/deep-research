from fastapi import FastAPI, Request
from pydantic import BaseModel
from research import deep_research
from report import write_final_answer, write_final_report
from config import PORT

app = FastAPI()


class ResearchInput(BaseModel):
    query: str
    depth: int = 3
    breadth: int = 3


@app.post("/api/research")
async def research_endpoint(payload: ResearchInput):
    try:
        print("\n[+] Running research...")
        result = await deep_research(
            query=payload.query,
            breadth=payload.breadth,
            depth=payload.depth,
        )

        learnings = result["learnings"]
        urls = result["visited_urls"]
        answer = write_final_answer(prompt=payload.query, learnings=learnings)

        return {
            "success": True,
            "answer": answer,
            "learnings": learnings,
            "visited_urls": urls,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@app.post("/api/generate-report")
async def report_endpoint(payload: ResearchInput):
    try:
        print("\n[+] Running research for report generation...")
        result = await deep_research(
            query=payload.query,
            breadth=payload.breadth,
            depth=payload.depth,
        )

        learnings = result["learnings"]
        urls = result["visited_urls"]
        report = write_final_report(prompt=payload.query, learnings=learnings, visited_urls=urls)

        return {
            "success": True,
            "report": report,
            "learnings": learnings,
            "visited_urls": urls,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
