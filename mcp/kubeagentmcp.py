"""
MCP Server for Kubernetes Tools — exposes K8s tools to Claude Desktop via MCP.
Run: python3 agentmcp.py
"""

import subprocess
from fastmcp import FastMCP

mcp = FastMCP("Kubernetes Tools")


@mcp.tool
def list_containers() -> str:
    """List all Docker containers (running and stopped)."""
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True)
    return result.stdout or result.stderr


@mcp.tool
def get_logs(container_name: str) -> str:
    """Get the last 50 lines of logs from a Docker container."""
    result = subprocess.run(
        ["docker", "logs", "--tail", "50", container_name],
        capture_output=True, text=True,
    )
    return result.stdout + result.stderr


@mcp.tool
def inspect_container(container_name: str) -> str:
    """Get detailed info about a Docker container (state, config, network)."""
    result = subprocess.run(
        ["docker", "inspect", container_name],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr


# --- Kubernetes tools ---

@mcp.tool
def list_pods(namespace: str = "default") -> str:
    """List all pods in a Kubernetes namespace with their status."""
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

@mcp.tool
def list_deployments(namespace: str = "default") -> str:
    """List all deployments in a Kubernetes namespace with their status."""
    result = subprocess.run(
        ["kubectl", "get", "deployments", "-n", namespace],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

@mcp.tool
def view_deployment(deployment_name: str, namespace: str = "default") -> str:
    """view currently running deployment configuration in a Kubernetes namespace."""
    result = subprocess.run(
        ["kubectl", "get", "deployment", deployment_name, "-n", namespace, "-o" "yaml"],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

@mcp.tool
def restart_deployment(deployment_name: str, namespace: str = "default") -> str:
    """Restart deployments in a Kubernetes namespace with their status."""
    result = subprocess.run(
        ["kubectl", "rollout", "restart", "deployment", deployment_name, "-n", namespace],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

@mcp.tool
def list_all(namespace: str = "default") -> str:
    """List all resources in a Kubernetes namespace with their status."""
    result = subprocess.run(
        ["kubectl", "get", "all", "-n", namespace],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr


@mcp.tool
def describe_pod(pod_name: str, namespace: str = "default") -> str:
    """Get detailed info about a Kubernetes pod including events and conditions."""
    result = subprocess.run(
        ["kubectl", "describe", "pod", pod_name, "-n", namespace],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

@mcp.tool
def logs_pod(pod_name: str, namespace: str = "default") -> str:
    """Get logs of a Kubernetes pod"""
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "-n", namespace],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

@mcp.tool
def previous_logs_pod(pod_name: str, namespace: str = "default") -> str:
    """Get logs of the pod preceding the current Kubernetes pod"""
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "--previous", "-n", namespace],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

@mcp.tool
def get_events(namespace: str = "default") -> str:
    """Get recent Kubernetes events in a namespace (useful for troubleshooting)."""
    result = subprocess.run(
        ["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"],
        capture_output=True, text=True,
    )
    return result.stdout or result.stderr

if __name__ == "__main__":
    mcp.run()

