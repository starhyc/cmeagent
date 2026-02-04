from app.services.report.template import ReportTemplate
from app.services.report.data_aggregator import ReportDataAggregator
from app.services.report.mermaid_embedder import MermaidDiagramEmbedder
from datetime import datetime

class MarkdownReportGenerator:
    def __init__(self):
        self.data_aggregator = ReportDataAggregator()
        self.mermaid_embedder = MermaidDiagramEmbedder()

    def generate_report(self, title: str, analysis_result: dict, timeline: list, call_chain: list, dependencies: dict) -> str:
        data = self.data_aggregator.aggregate_data(analysis_result, timeline, call_chain)

        report = f"# {title}\n\n"
        report += f"## Executive Summary\n\n{data['overview']}\n\n"
        report += f"## Problem Overview\n\n### Symptoms\n"
        for symptom in data['symptoms']:
            report += f"- {symptom}\n"

        report += f"\n### Timeline\n\n"
        report += self.mermaid_embedder.embed_timeline_diagram(timeline)

        report += f"\n\n## Root Cause Analysis\n\n"
        report += data['root_cause'].get('analysis', 'No analysis available')

        report += f"\n\n## Technical Details\n\n### Call Chain\n\n"
        report += self.mermaid_embedder.embed_call_chain_diagram(dependencies)

        report += f"\n\n## Recommended Solutions\n\n"
        for solution in data['solutions']:
            report += f"{solution}\n\n"

        report += f"## Prevention Measures\n\n"
        for improvement in data['improvements']:
            report += f"- {improvement}\n"

        report += f"\n---\n*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        report += f"*Confidence Score: {data['confidence']:.0%}*\n"

        return report
