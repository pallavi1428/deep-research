import asyncio
import sys
from datetime import datetime
from pathlib import Path
from feedback import generate_feedback
from research import deep_research
from report import write_final_answer, write_final_report
from pdf_generator import PDFReportGenerator

def ask(question: str, default: str = "") -> str:
    try:
        val = input(f"{question} ").strip()
        return val if val else default
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)

async def main():
    query = ask("What would you like to research?")
    breadth = int(ask("Enter research breadth (2-10, default 4):", "4"))
    depth = int(ask("Enter research depth (1-5, default 2):", "2"))
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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if mode == "report":
        print("\nWriting report...")
        report = write_final_report(combined_query, learnings, visited_urls)
        md_filename = f"report_{timestamp}.md"
        pdf_filename = f"report_{timestamp}.pdf"
        
        # Save Markdown
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(report)
            
        # Generate PDF
        try:
            pdf_gen = PDFReportGenerator()
            pdf_gen.generate_from_markdown(report, pdf_filename)
            print(f"✅ Report saved to {md_filename} and {pdf_filename}")
        except Exception as e:
            print(f"⚠️ PDF generation failed: {str(e)}")
            print(f"✅ Markdown report saved to {md_filename}")
    else:
        print("\nWriting final answer...")
        answer = write_final_answer(combined_query, learnings)
        md_filename = f"answer_{timestamp}.md"
        pdf_filename = f"answer_{timestamp}.pdf"
        
        # Save Markdown
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(answer)
            
        # Generate PDF
        try:
            pdf_gen = PDFReportGenerator()
            pdf_gen.generate_from_markdown(answer, pdf_filename)
            print(f"✅ Answer saved to {md_filename} and {pdf_filename}")
        except Exception as e:
            print(f"⚠️ PDF generation failed: {str(e)}")
            print(f"✅ Markdown answer saved to {md_filename}")

if __name__ == "__main__":
    asyncio.run(main())