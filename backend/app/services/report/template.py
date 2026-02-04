class ReportTemplate:
    @staticmethod
    def generate_template(title: str) -> str:
        return f"""# {title}

## Executive Summary

[Brief overview of the problem and findings]

## Problem Overview

### Symptoms
- [List of observed symptoms]

### Timeline
[When the issue occurred and key events]

## Root Cause Analysis

### Primary Cause
[Main cause of the issue]

### Contributing Factors
- [Factor 1]
- [Factor 2]

## Technical Details

### Error Logs
[Relevant error messages and stack traces]

### Call Chain
[Module interaction flow]

### Code Locations
[Relevant code sections]

## Recommended Solutions

### Immediate Fix
[Quick fix to resolve the issue]

### Long-term Improvements
- [Improvement 1]
- [Improvement 2]

## Prevention Measures

[Steps to prevent similar issues]

## Glossary

[Technical terms and definitions]

---
*Generated on: {{timestamp}}*
*Confidence Score: {{confidence}}*
"""
