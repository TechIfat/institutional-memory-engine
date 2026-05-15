"""
Institutional Memory Engine (Raw SDK Orchestration)
Demonstrates Native Evaluator-Optimiser loop, Prompt Caching, and Forced JSON Tool Use.
"""
import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

load_dotenv(".env.local")
console = Console()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL_NAME = "claude-sonnet-4-6"

# ---------------------------------------------------------
# 1. NATIVE TOOL SCHEMA (Using Pydantic for generation)
# ---------------------------------------------------------
class RiskEvaluation(BaseModel):
    is_compliant: bool = Field(description="True ONLY if the draft matches historical deal precedents.")
    score: int = Field(description="Risk score out of 100.")
    redlines: list[str] = Field(description="Specific clauses that violate our institutional memory. Empty if compliant.")

# Convert Pydantic model to Anthropic's native JSON Schema format
evaluation_tool = {
    "name": "evaluate_risk",
    "description": "Evaluate the drafted term sheet against historical bank precedents.",
    "input_schema": RiskEvaluation.model_json_schema()
}

# ---------------------------------------------------------
# 2. THE RAW ORCHESTRATOR
# ---------------------------------------------------------
def run_institutional_memory_loop(new_application: str):
    console.print("\n[bold cyan]🏦 INITIATING INSTITUTIONAL MEMORY ENGINE...[/bold cyan]\n")
    
    # Read the historical data
    with open("data/synthetic/historical_deals.txt", "r") as f:
        raw_history = f.read()
        
    # THE ARCHITECT'S HACK: Pad the history so it exceeds 1024 tokens to trigger Anthropic's Cache!
    padded_history = raw_history + ("\n[ARCHIVE DATA] " * 1000)

    # We build the EXACT SAME system prompt for both agents. 
    # Because the prefix is identical, the Evaluator hits the Underwriter's cache!
    shared_system_prompt = [
        {
            "type": "text",
            "text": "You are a Senior Corporate Banking AI. Here is the bank's Institutional Memory of past deals:\n\n" + padded_history,
            "cache_control": {"type": "ephemeral"} # <--- THE FINOPS MAGIC
        }
    ]

    # Manual Context Management (The "State")
    conversation_history = [
        {"role": "user", "content": f"Draft a concise term sheet for this new application: {new_application}. Include the DSCR."}
    ]

    iteration = 0
    max_iterations = 3

    while iteration < max_iterations:
        iteration += 1
        console.print(f"\n✍️  [bold blue]UNDERWRITER (Iteration {iteration}):[/bold blue] Drafting term sheet...")
        
        # --- AGENT 1: THE UNDERWRITER ---
        underwriter_response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1000,
            temperature=0,
            system=shared_system_prompt,
            messages=conversation_history
        )
        
        draft_text = underwriter_response.content[0].text
        console.print(Panel(draft_text, title="Drafted Term Sheet", border_style="blue"))
        
        # Save output to context
        conversation_history.append({"role": "assistant", "content": draft_text})

        # --- AGENT 2: THE EVALUATOR ---
        console.print("🧐 [bold red]EVALUATOR:[/bold red] Checking draft against Institutional Memory...")
        
        evaluator_messages = conversation_history + [
            {"role": "user", "content": "Evaluate this draft against our historical deals. Use your tool to output the strict JSON compliance result."}
        ]

        evaluator_response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1000,
            temperature=0,
            system=shared_system_prompt,
            messages=evaluator_messages,
            tools=[evaluation_tool],
            tool_choice={"type": "tool", "name": "evaluate_risk"} # FORCED JSON!
        )

        # 3. NATIVE TOOL PARSING & METRICS
        usage = evaluator_response.usage
        console.print(f"📊 [dim]FinOps Metric - Cache READ Tokens: {getattr(usage, 'cache_read_input_tokens', 0)}[/dim]")

        # Extract the JSON payload
        eval_data = None
        for block in evaluator_response.content:
            if block.type == "tool_use":
                eval_data = block.input
                break
                
        if not eval_data:
            console.print("[bold red]🚨 SYSTEM ERROR: Evaluator failed to use the JSON tool.[/bold red]")
            break

        # 4. RAW ROUTING LOGIC
        if eval_data["is_compliant"]:
            console.print(f"[bold green]✅ APPROVED! Score: {eval_data['score']}/100[/bold green]")
            break
        else:
            console.print(f"[bold red]❌ REJECTED. Score: {eval_data['score']}/100[/bold red]")
            for redline in eval_data["redlines"]:
                console.print(f"  - 🚨 [italic]{redline}[/italic]")
            
            # Feed redlines back to Underwriter!
            conversation_history.append({
                "role": "user", 
                "content": f"The draft was rejected based on historical precedent. Fix these exact issues: {json.dumps(eval_data['redlines'])}. Output the rewritten term sheet."
            })

    if iteration == max_iterations:
        console.print("[bold red]🚨 CIRCUIT BREAKER TRIPPED: Max iterations reached.[/bold red]")

if __name__ == "__main__":
    # THE TRAP: We request a Retail loan with a 1.20x DSCR. 
    # The Institutional Memory explicitly says Retail loans require 1.25x!
    test_application = "Client wants a £20,000,000 commercial loan in the Retail sector. We are proposing a DSCR of 1.20x."
    run_institutional_memory_loop(test_application)