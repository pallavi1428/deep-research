import asyncio
import sys
import gradio as gr
from feedback import generate_feedback
from research import deep_research
from report import write_final_answer, write_final_report

# Async Gradio works natively, no need to wrap the event loop.
async def process_research(query, breadth, depth, mode, followup_answers):
    if mode == "report":
        questions = generate_feedback(query)
        combined_query = f"Initial Query: {query}\n\nFollow-up Questions and Answers:\n"
        combined_query += "\n".join(f"Q: {q}\nA: {a}" for q, a in zip(questions, followup_answers))
    else:
        combined_query = query

    result = await deep_research(
        query=combined_query,
        depth=depth,
        breadth=breadth,
    )

    learnings = result["learnings"]
    visited_urls = result["visited_urls"]

    if mode == "report":
        report = write_final_report(combined_query, learnings, visited_urls)
        file_path = "report.md"
    else:
        report = write_final_answer(combined_query, learnings)
        file_path = "answer.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report)

    learnings_display = "\n".join(f"- {l}" for l in learnings[:10])
    urls_display = "\n".join(f"- {u}" for u in visited_urls[:5])

    return learnings_display, urls_display, file_path

with gr.Blocks() as app:
    gr.Markdown("# AI Research Assistant 🔍")
    
    with gr.Row():
        query_input = gr.Textbox(label="What would you like to research?", placeholder="Enter your query, e.g., Robotics")
    
    with gr.Row():
        breadth_input = gr.Slider(2, 10, value=4, step=1, label="Research Breadth")
        depth_input = gr.Slider(1, 5, value=2, step=1, label="Research Depth")
    
    with gr.Row():
        mode_input = gr.Radio(["report", "answer"], label="Select Mode", value="report")
    
    with gr.Row():
        followup_answers_input = gr.Textbox(
            label="Follow-up Answers (if any, comma separated)", 
            placeholder="Answer1, Answer2, Answer3... (leave blank if not applicable)"
        )

    run_button = gr.Button("Start Research 🚀")

    learnings_output = gr.Textbox(label="Key Learnings", lines=10)
    urls_output = gr.Textbox(label="Visited URLs", lines=5)
    file_output = gr.File(label="Download Result")

    async def on_run(query, breadth, depth, mode, followup_answers):
        answers = [a.strip() for a in followup_answers.split(",")] if followup_answers else []
        return await process_research(query, breadth, depth, mode, answers)

    run_button.click(
        on_run,
        inputs=[query_input, breadth_input, depth_input, mode_input, followup_answers_input],
        outputs=[learnings_output, urls_output, file_output]
    )

if __name__ == "__main__":
    app.launch()
