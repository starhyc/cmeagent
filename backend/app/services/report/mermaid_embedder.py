class MermaidDiagramEmbedder:
    def __init__(self):
        pass

    def embed_timeline_diagram(self, timeline: list) -> str:
        diagram = "```mermaid\ngantt\n    title Event Timeline\n    dateFormat HH:mm:ss\n"

        for event in timeline[:10]:
            timestamp = event.get('timestamp')
            if timestamp:
                time_str = timestamp.strftime('%H:%M:%S')
                module = event.get('module', 'Unknown')
                diagram += f"    {module} : {time_str}, 1s\n"

        diagram += "```"
        return diagram

    def embed_call_chain_diagram(self, dependencies: dict) -> str:
        diagram = "```mermaid\ngraph TD\n"

        for source, targets in dependencies.items():
            for target in targets:
                diagram += f"    {source} --> {target}\n"

        diagram += "```"
        return diagram

    def embed_flow_diagram(self, mermaid_code: str) -> str:
        if not mermaid_code.startswith('```mermaid'):
            return f"```mermaid\n{mermaid_code}\n```"
        return mermaid_code
