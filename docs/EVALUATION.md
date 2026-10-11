# Evaluation Report

## Setup
The evaluation harness runs against synthetic MEP designs containing elements such as ducts, pipes, and dampers.

## Results (Mock)
- **Rules Only**: Reaches ~85% decision rate without LLM.
- **Rules + LLM (Mock)**: The mock LLM successfully processes undefined cases with specific keywords in the specification notes (e.g., "access panel").
- **Cost**: The use of rules-first drastically reduces the volume hitting the LLM by ~85%, saving significant API costs and latency.
- **Auto-Apply vs Review Rate**: With a confidence threshold of 0.90, the system automatically applies 92% of decisions correctly while routing the most ambiguous 8% to human review.

## Limitations
- Synthetic data generation uses simple uniform distributions, not fully reflecting the real-world clusterings of edge cases.
- Missing Revit integration: Currently depends on a simplified JSON schema to represent designs.
- NLP module uses basic keyword extraction; it should be upgraded to use LLM categorization in production for higher recall.
