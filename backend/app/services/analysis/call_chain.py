from sqlalchemy.orm import Session
from app.models.database import Log
from typing import List, Dict
import re

class CallChainAnalyzer:
    def __init__(self, db: Session):
        self.db = db

    def analyze_call_chain(self, session_id: str, start_timestamp) -> List[Dict]:
        logs = self.db.query(Log).filter(
            Log.session_id == session_id,
            Log.timestamp >= start_timestamp
        ).order_by(Log.timestamp).limit(100).all()

        call_chain = []
        for log in logs:
            if log.module:
                call_chain.append({
                    'timestamp': log.timestamp,
                    'module': log.module,
                    'level': log.level,
                    'message': log.message
                })

        return call_chain

    def extract_module_dependencies(self, call_chain: List[Dict]) -> Dict:
        dependencies = {}
        for i in range(len(call_chain) - 1):
            current = call_chain[i]['module']
            next_module = call_chain[i + 1]['module']
            if current != next_module:
                if current not in dependencies:
                    dependencies[current] = set()
                dependencies[current].add(next_module)

        return {k: list(v) for k, v in dependencies.items()}
