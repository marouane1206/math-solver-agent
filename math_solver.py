#!/usr/bin/env python3
"""
Interactive Math Problem Solver using Claude 4 Code Execution Tool

This application allows users to ask math questions in natural language,
gets solutions using Claude's code execution capabilities, and saves
both visualizations and detailed markdown reports.
"""

import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any
from anthropic import Anthropic


class MathSolver:
    def __init__(self, api_key: str = None):
        """Initialize the Math Solver with Anthropic client."""
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "Please set ANTHROPIC_API_KEY environment variable or provide api_key"
                )

        # Initialize client with code execution and files API
        self.client = Anthropic(
            api_key=api_key,
            default_headers={
                "anthropic-beta": "code-execution-2025-05-22,files-api-2025-04-14"
            },
        )

        # Create output directories
        self.output_dir = Path("math_solver_output")
        self.images_dir = self.output_dir / "images"
        self.reports_dir = self.output_dir / "reports"

        self.output_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)

        print(f"📁 Output directories created:")
        print(f"   • Images: {self.images_dir}")
        print(f"   • Reports: {self.reports_dir}")

    def solve_problem(self, question: str) -> Dict[str, Any]:
        """
        Send a math question to Claude and get solution with code execution.

        Args:
            question: The math question in natural language

        Returns:
            Dictionary containing the response and metadata
        """
        print(f"\n🤔 Thinking about: {question}")

        try:
            # Use streaming to show real-time progress
            with self.client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Solve this math problem using code execution:

Problem: {question}

Please:
1. Solve the problem with actual Python code
2. Create visualizations using matplotlib if helpful
3. Save any plots as PNG files using plt.savefig()
4. Show your calculations step by step
5. Use descriptive filenames for saved plots

Execute Python code to solve this problem.""",
                    }
                ],
                tools=[{"type": "code_execution_20250522", "name": "code_execution"}],
            ) as stream:
                print("\n💭 Claude is working...")

                # Process streaming events and show progress
                for event in stream:
                    if event.type == "content_block_start":
                        if hasattr(event.content_block, "type"):
                            if event.content_block.type == "text":
                                print("\n📝 Response:", end=" ", flush=True)
                            elif event.content_block.type == "server_tool_use":
                                print(f"\n🔧 Using tool: {event.content_block.name}")

                    elif event.type == "content_block_delta":
                        if hasattr(event.delta, "text"):
                            print(event.delta.text, end="", flush=True)

                    elif event.type == "content_block_stop":
                        print("", flush=True)  # New line

                    elif event.type == "message_delta":
                        if hasattr(event.delta, "stop_reason"):
                            print(f"\n✅ Completed: {event.delta.stop_reason}")

                # Get the final message
                final_message = stream.get_final_message()

                return {
                    "response": final_message,
                    "question": question,
                    "timestamp": datetime.datetime.now().isoformat(),
                }

        except Exception as e:
            print(f"❌ Error solving problem: {e}")
            return None

    def extract_files_from_response(self, response) -> List[str]:
        """Extract file IDs from Claude's response."""
        file_ids = []

        for item in response.content:
            if item.type == "code_execution_tool_result":
                content_item = item.content

                if isinstance(content_item, dict):
                    if content_item.get("type") == "code_execution_result":
                        content_list = content_item.get("content", [])

                        for file_item in content_list:
                            if isinstance(file_item, dict) and "file_id" in file_item:
                                file_ids.append(file_item["file_id"])

        return file_ids

    def download_files(self, file_ids: List[str]) -> List[str]:
        """Download files created by code execution to local storage."""
        downloaded_files = []

        for file_id in file_ids:
            try:
                # Get file metadata and download content
                file_metadata = self.client.beta.files.retrieve_metadata(file_id)
                filename = file_metadata.filename

                file_content = self.client.beta.files.download(file_id)
                local_path = self.images_dir / filename
                file_content.write_to_file(str(local_path))

                downloaded_files.append(str(local_path))
                print(f"✅ Downloaded: {filename}")

            except Exception as e:
                print(f"❌ Error downloading file {file_id}: {e}")

        return downloaded_files

    def extract_code_blocks(self, response) -> List[str]:
        """Extract all code blocks from the response."""
        code_blocks = []

        for item in response.content:
            if item.type == "server_tool_use" and item.name == "code_execution":
                if (
                    hasattr(item, "input")
                    and isinstance(item.input, dict)
                    and "code" in item.input
                ):
                    code_blocks.append(item.input["code"])

        return code_blocks

    def generate_markdown_report(
        self, result: Dict[str, Any], downloaded_files: List[str]
    ) -> str:
        """Generate a comprehensive markdown report of the solution."""
        response = result["response"]
        question = result["question"]
        timestamp = result["timestamp"]

        # Extract text content and code blocks
        text_content = []
        code_blocks = self.extract_code_blocks(response)

        for item in response.content:
            if item.type == "text":
                text_content.append(item.text)

        # Generate filename with timestamp
        safe_question = "".join(
            c for c in question[:50] if c.isalnum() or c in (" ", "-", "_")
        ).strip()
        filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_question.replace(' ', '_')}.md"
        filepath = self.reports_dir / filename

        # Create markdown content
        markdown_content = f"""# Math Problem Solution Report

**Generated:** {timestamp}
**Question:** {question}

---

## Problem Statement

{question}

---

## Solution

"""

        # Add the main explanation
        for text in text_content:
            markdown_content += f"{text}\n\n"

        # Add code sections
        if code_blocks:
            markdown_content += "---\n\n## Code Used\n\n"
            for i, code in enumerate(code_blocks, 1):
                markdown_content += f"### Code Block {i}\n\n```python\n{code}\n```\n\n"

        # Add images section
        if downloaded_files:
            markdown_content += "---\n\n## Generated Visualizations\n\n"
            for file_path in downloaded_files:
                filename = Path(file_path).name
                relative_path = f"../images/{filename}"
                markdown_content += f"![{filename}]({relative_path})\n\n"

        # Add footer
        markdown_content += f"""---

## Report Details

- **Generated by:** Claude 4 Math Solver
- **Model:** claude-sonnet-4-20250514
- **Timestamp:** {timestamp}
- **Files created:** {len(downloaded_files)} visualization(s)

---

*This report was automatically generated using Claude's code execution capabilities.*
"""

        # Save the report
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return str(filepath)

    def run_interactive_session(self):
        """Run the main interactive session loop."""
        print("🧮 Interactive Math Problem Solver with Claude 4")
        print("=" * 60)
        print("Ask me any math question and I'll solve it step by step!")
        print("I can handle algebra, calculus, statistics, geometry, and more.")
        print("Type 'quit', 'exit', or 'q' to end the session.")
        print("=" * 60)

        session_count = 0

        while True:
            try:
                # Get user input
                question = input(f"\n📝 Question #{session_count + 1}: ").strip()

                if question.lower() in ["quit", "exit", "q"]:
                    print("\n👋 Thanks for using the Math Solver! Goodbye!")
                    break

                if not question:
                    print("Please enter a question.")
                    continue

                session_count += 1

                # Solve the problem
                result = self.solve_problem(question)
                if not result:
                    continue

                # Extract and download any files created
                file_ids = self.extract_files_from_response(result["response"])
                downloaded_files = []
                if file_ids:
                    print(f"📥 Downloading {len(file_ids)} file(s)...")
                    downloaded_files = self.download_files(file_ids)

                # Generate markdown report
                print(f"📝 Generating report...")
                report_path = self.generate_markdown_report(result, downloaded_files)

                print(f"\n✅ Solution complete!")
                print(f"📄 Report saved: {report_path}")
                if downloaded_files:
                    print(f"🖼️  Visualizations: {len(downloaded_files)} file(s) saved")

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                print("Please try again with a different question.")


def main():
    """Main entry point for the application."""
    try:
        solver = MathSolver()
        solver.run_interactive_session()
    except Exception as e:
        print(f"❌ Failed to initialize Math Solver: {e}")
        print("Make sure you have set the ANTHROPIC_API_KEY environment variable.")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
