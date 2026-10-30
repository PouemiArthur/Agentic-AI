"""
MCP Server for Linux CLI navigation tools exposed to Claude Desktop via MCP.
Run: python3 naviagentmcp.py
"""
import os
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent as create_react_agent


@tool
def list_files(path: str = ".") -> str:
    """list all files and sub-directories in the given directory"""
    path = os.path.expanduser(path)
    if not os.path.isdir(path):
        return f"Error: {path} is not a directory"
    entries = sorted(os.listdir(path))
    return "\n".join(
        f"{e}/" if os.path.isdir(os.path.join(path, e)) else e
        for e in entries
    )


@tool
def read_file(files: str) -> str:
    """Read or view files content"""
    result = subprocess.run(
        ["cat", files],
        capture_output=True, text=True,
    )
    return result.stdout + result.stderr

llm = ChatOllama(model="gemma4", temperature=0)
tools = [ list_files, read_file ]
agent = create_react_agent(llm, tools)

print("\nPJrNavi")
print("-" * 40)
print("I can navigate across directories and read files")
print("Type 'quit' to exit.\n")

while True:
    question = input("> ").strip()
    if question.lower() in ("quit", "exit", "q"):
        break
    if not question:
        continue

    print("\nThinking...\n")
    result = agent.invoke({"messages": [("user", question)]})
    print(result["messages"][-1].content)
    print()

