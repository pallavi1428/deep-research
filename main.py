import asyncio
import sys
from feedback import generate_feedback
from research import deep_research
from report import write_final_answer, write_final_report

def ask(question: str, default: str = "") -> str:
    try:
        val = input(f"{question} ").strip()
        return val if val else default
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)


async def main():
    query = ask("What would you like to research?")
    breadth = int(ask("Enter research breadth (2–10, default 4):", "4"))
    depth = int(ask("Enter research depth (1–5, default 2):", "2"))
    mode = ask("Do you want a long report or a short answer? (report/answer)", "report").lower()

    if mode == "report":
        print("\nGenerating follow-up questions...")
        questions = generate_feedback(query)
        answers = []
        for q in questions:
            a = ask(f"{q}\nYour answer:")
            answers.append(a)

        combined_query = f"Initial Query: {query}\n\nFollow-up Questions and Answers:\n"
        combined_query += "\n".join(f"Q: {q}\nA: {a}" for q, a in zip(questions, answers))
    else:
        combined_query = query

    print("\nStarting research...\n")
    result = await deep_research(
        query=combined_query,
        depth=depth,
        breadth=breadth,
    )

    learnings = result["learnings"]
    visited_urls = result["visited_urls"]

    print(f"\nLearnings ({len(learnings)}):")
    print("\n".join(f"- {l}" for l in learnings[:10]))

    print(f"\nVisited URLs ({len(visited_urls)}):")
    print("\n".join(f"- {u}" for u in visited_urls[:5]))

    if mode == "report":
        print("\nWriting report...")
        report = write_final_report(combined_query, learnings, visited_urls)
        with open("report.md", "w", encoding="utf-8") as f:
            f.write(report)
        print("✅ Report saved to report.md")
    else:
        print("\nWriting final answer...")
        answer = write_final_answer(combined_query, learnings)
        with open("answer.md", "w", encoding="utf-8") as f:
            f.write(answer)
        print("✅ Answer saved to answer.md")


if __name__ == "__main__":
    asyncio.run(main())
