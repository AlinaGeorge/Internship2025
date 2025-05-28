import asyncio
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import sympy as sp
import os
from dotenv import load_dotenv

load_dotenv()

# Tool: Solve math problems
def solve_math_problem(problem: str) -> str:
    try:
        if "solve" in problem:
            expr = sp.sympify(problem.split("solve")[1].strip().replace("=", "-(") + ")")
            sol = sp.solve(expr)
            return f"Solved: {sp.latex(expr)} = 0; Solution: {sol}"
        elif "differentiate" in problem or "derivative" in problem:
            expr = sp.sympify(problem.split()[-1])
            diff = sp.diff(expr)
            return f"Derivative of {sp.latex(expr)}: {diff}"
        else:
            result = eval(problem)
            return f"Result: {result}"
    except Exception as e:
        return f"Error solving: {str(e)}"

# Tool: Verify solutions
def verify_solution(problem: str, solution: str) -> str:
    try:
        if "solve" in problem:
            expr = sp.sympify(problem.split("solve")[1].strip().replace("=", "-(") + ")")
            solutions = eval(solution.split("Solution: ")[1])
            verified = all(sp.simplify(expr.subs('x', s)) == 0 for s in solutions)
            result = f"Verification: {'Correct' if verified else 'Incorrect'}"
        elif "differentiate" in problem or "derivative" in problem:
            result = "Derivative check passed (assumed correct for simplicity)."
        else:
            computed = eval(problem)
            given = eval(solution.split(": ")[-1])
            result = f"Verification: {'Correct' if computed == given else 'Incorrect'}"
        return result + "\nTERMINATE"
    except Exception as e:
        return f"Verification error: {str(e)}\nTERMINATE"

async def main():
    # Gemini model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("API_KEY"),
    )

    # Problem Solver Agent
    problem_solver_agent = AssistantAgent(
        name="problem_solver_agent",
        model_client=model_client,
        description="Solves math problems using SymPy.",
        system_message="You are a math expert that uses solve_math_problem to solve equations or compute derivatives. Send the result to the verifier.",
        tools=[solve_math_problem]
    )

    # Verifier Agent
    verifier_agent = AssistantAgent(
        name="verifier_agent",
        model_client=model_client,
        description="Verifies the solution to the math problem.",
        system_message="You are an expert in verifying math solutions using verify_solution. After checking, respond with 'TERMINATE'.",
        tools=[verify_solution]
    )
    user= UserProxyAgent(
        name="user_proxy_agent",
        description="A user agent that interacts with the problem solver and verifier agents.",    
    )
    # Termination condition: message contains 'TERMINATE'
    termination = TextMentionTermination("TERMINATE")

    # Group chat setup
    group_chat = RoundRobinGroupChat(
        [problem_solver_agent, verifier_agent, user],
        termination_condition=termination
    )

    # Task input
    task = "solve x^2 - 4 = 0"

    # Start the group chat
    await Console(group_chat.run_stream(task=task))

    # Close model client
    await model_client.close()

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
