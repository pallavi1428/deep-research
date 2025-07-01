# main.py
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from feedback import generate_feedback
from research import deep_research
from report import write_final_answer, write_final_report
from fpdf import FPDF
from typing import List, Tuple

# Load environment variables
load_dotenv()

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('DejaVu', '', 'DejaVuSans.ttf')
        self.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf')
        self.set_font('DejaVu', '', 12)
    
    def header(self):
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, 'Comprehensive Research Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def section_title(self, title):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, title, 0, 1)
        self.ln(2)
    
    def section_subtitle(self, subtitle):
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 8, subtitle, 0, 1)
        self.ln(2)
    
    def body_text(self, text):
        self.set_font('DejaVu', '', 12)
        self.multi_cell(0, 6, text)
        self.ln(4)
    
    def bullet_point(self, text):
        self.set_font('DejaVu', '', 12)
        self.cell(10)
        self.multi_cell(0, 6, "• " + text)
        self.ln(2)

class ResearchAssistant:
    def __init__(self):
        self.validate_env_vars()
        
    def validate_env_vars(self):
        """Check required environment variables are set"""
        required_vars = ['FIRECRAWL_KEY', 'OPENAI_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    async def conduct_research(self, query: str, breadth: int, depth: int, mode: str):
        """Execute full research workflow"""
        print("\nInitializing research engine...")
        
        # Generate follow-up questions if in report mode
        if mode == "report":
            print("\nDeveloping research framework...")
            questions = generate_feedback(query)
            answers = []
            for q in questions:
                answer = input(f"\nFollow-up Question: {q}\nYour answer: ")
                answers.append(answer)
            
            combined_query = self._build_research_query(query, questions, answers)
        else:
            combined_query = query

        # Conduct deep research
        print("\nGathering authoritative sources...")
        result = await deep_research(
            query=combined_query,
            depth=depth,
            breadth=breadth,
        )

        # Process findings
        print("\nAnalyzing collected data...")
        learnings = result["learnings"]
        visited_urls = result["visited_urls"]

        # Generate output files
        print("\nCompiling final report...")
        md_content, md_path = self._generate_markdown_output(
            mode, combined_query, learnings, visited_urls
        )
        pdf_path = self._generate_pdf_output(
            mode, combined_query, learnings, visited_urls
        )

        # Display summary
        self._display_summary(learnings, visited_urls, md_path, pdf_path)

    def _build_research_query(self, query: str, questions: List[str], answers: List[str]) -> str:
        """Build comprehensive research query with follow-ups"""
        combined = f"# Comprehensive Research Request\n\n## Primary Inquiry\n{query}\n\n"
        if questions:
            combined += "## Follow-up Investigations\n"
            combined += "\n".join(f"### {q}\n{a}\n" for q, a in zip(questions, answers))
        return combined

    def _generate_markdown_output(
        self,
        mode: str,
        combined_query: str,
        learnings: List[str],
        visited_urls: List[str]
    ) -> Tuple[str, str]:
        """Generate markdown output file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if mode == "report":
            content = self._generate_full_report(combined_query, learnings, visited_urls)
            filename = f"research_report_{timestamp}.md"
        else:
            content = write_final_answer(combined_query, learnings)
            filename = f"research_answer_{timestamp}.md"
        
        Path(filename).write_text(content, encoding="utf-8")
        return content, filename

    def _generate_pdf_output(
        self,
        mode: str,
        combined_query: str,
        learnings: List[str],
        visited_urls: List[str]
    ) -> str:
        """Generate PDF output file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_report_{timestamp}.pdf" if mode == "report" else f"research_answer_{timestamp}.pdf"
        
        pdf = PDFReport()
        pdf.add_page()
        
        if mode == "report":
            self._create_full_pdf_report(pdf, combined_query, learnings, visited_urls)
        else:
            self._create_pdf_answer(pdf, combined_query, learnings)
        
        pdf.output(filename)
        return filename

    def _create_full_pdf_report(self, pdf: PDFReport, query: str, learnings: List[str], urls: List[str]):
        """Generate a professional PDF report"""
        # Title Page
        pdf.set_font('DejaVu', 'B', 20)
        pdf.cell(0, 40, "Comprehensive Research Report", 0, 1, 'C')
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(0, 10, query.split('.')[0], 0, 1, 'C')
        pdf.ln(20)
        pdf.set_font('DejaVu', '', 10)
        pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%B %d, %Y')}", 0, 1, 'C')
        pdf.add_page()
        
        # Executive Summary
        pdf.section_title("Executive Summary")
        pdf.body_text(f"This report provides an in-depth analysis of {query.split('.')[0]}. "
                     "It covers key aspects, technical details, and implications based on comprehensive research.")
        
        # Organized sections
        sections = self._organize_learnings(learnings)
        for section_title, section_content in sections.items():
            if section_content:
                pdf.add_page()
                pdf.section_title(section_title)
                for item in section_content:
                    pdf.bullet_point(self._format_learning_item(item))
        
        # References
        pdf.add_page()
        pdf.section_title("References")
        for url in urls[:15]:
            pdf.bullet_point(url)

    def _create_pdf_answer(self, pdf: PDFReport, query: str, learnings: List[str]):
        """Generate concise PDF answer"""
        pdf.set_font('DejaVu', 'B', 16)
        pdf.cell(0, 10, "Research Summary", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font('DejaVu', '', 12)
        pdf.multi_cell(0, 6, f"Topic: {query}")
        pdf.ln(5)
        
        for learning in learnings[:15]:  # Limit to top 15 learnings for concise answer
            pdf.bullet_point(self._format_learning_item(learning))

    def _generate_full_report(self, query: str, learnings: List[str], urls: List[str]) -> str:
        """Generate a professional report with proper structure"""
        report = f"""# Comprehensive Research Report\n\n"""
        report += f"""## Executive Summary\n\nThis report provides an in-depth analysis of {query.split('.')[0]}. """
        report += """It covers key aspects, technical details, and implications based on comprehensive research.\n\n"""
        
        # Organize learnings into sections
        sections = self._organize_learnings(learnings)
        
        for section_title, section_content in sections.items():
            if section_content:  # Only include sections with content
                report += f"## {section_title}\n\n"
                report += "\n".join(f"- {self._format_learning_item(item)}" for item in section_content)
                report += "\n\n"
        
        # Add sources section
        report += "## References\n\n"
        report += "\n".join(f"- {url}" for url in urls[:15])
        
        return report

    def _organize_learnings(self, learnings: List[str]) -> dict:
        """Organize learnings into logical sections"""
        sections = {
            "Historical Context": [],
            "Technical Specifications": [],
            "Current Implications": [],
            "Future Considerations": [],
            "Key Findings": []
        }
        
        # Simple heuristic to categorize learnings
        for learning in learnings:
            lower_learning = learning.lower()
            if any(word in lower_learning for word in ['history', 'developed', 'origin']):
                sections["Historical Context"].append(learning)
            elif any(word in lower_learning for word in ['technical', 'design', 'mechanism']):
                sections["Technical Specifications"].append(learning)
            elif any(word in lower_learning for word in ['current', 'today', 'modern']):
                sections["Current Implications"].append(learning)
            elif any(word in lower_learning for word in ['future', 'will', 'potential']):
                sections["Future Considerations"].append(learning)
            else:
                sections["Key Findings"].append(learning)
                
        return sections

    def _format_learning_item(self, item: str) -> str:
        """Format individual learning item"""
        if ":" in item:
            key, value = item.split(":", 1)
            return f"{key.strip()}: {value.strip()}"
        return item

    def _display_summary(self, learnings: List[str], urls: List[str], md_path: str, pdf_path: str):
        """Display research summary to console"""
        print("\nResearch Summary:")
        print("=" * 50)
        
        sections = self._organize_learnings(learnings)
        for section_title, section_content in sections.items():
            if section_content:
                print(f"\n{section_title}:")
                print("-" * len(section_title))
                for item in section_content[:5]:
                    print(f"  • {self._format_learning_item(item)}")
        
        print("\nTop Sources:")
        print("-" * 12)
        for url in urls[:5]:
            print(f"  • {self._get_domain(url)}")
        
        print("\n" + "=" * 50)
        print(f"\n✅ Markdown output saved to: {md_path}")
        print(f"✅ PDF output saved to: {pdf_path}\n")

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL"""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return domain.replace("www.", "")


def get_user_input(prompt: str, default: str = "", is_int: bool = False):
    """Get user input with optional default value"""
    try:
        val = input(f"{prompt} [{default}]: " if default else f"{prompt}: ").strip()
        val = val or default
        return int(val) if is_int else val
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)


async def main():
    print("\n" + "=" * 50)
    print("Advanced Research Assistant (CLI Version)")
    print("=" * 50 + "\n")
    
    assistant = ResearchAssistant()
    
    query = get_user_input("What would you like to research?")
    breadth = get_user_input("Research breadth (2-10)", "4", is_int=True)
    depth = get_user_input("Research depth (1-5)", "2", is_int=True)
    mode = get_user_input("Output type (report/answer)", "report").lower()

    await assistant.conduct_research(
        query=query,
        breadth=breadth,
        depth=depth,
        mode=mode
    )


if __name__ == "__main__":
    asyncio.run(main())