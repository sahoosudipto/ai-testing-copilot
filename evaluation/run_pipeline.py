# run_pipeline.py

import pandas as pd
from app.main import get_ai_response
from evaluation.evaluator import evaluate_response

# Load test cases
# df = pd.read_csv("data/test_cases.csv")
df = pd.read_csv("data/final_dataset.csv")

results = [] # To store results of each test case

for index, row in df.iterrows():
    query = row["query"] # Assuming the CSV has a column named 'query'. Extracting query from the CSV file for each test case.
    
    print(f"\nRunning Test Case: {query}")
    
    # Get AI response for the query
    response = get_ai_response(query)
    # Print the response for debugging purposes
    evaluation = evaluate_response(query, response)
    
    # Extract score
    lines = evaluation.split("\n") # Split the evaluation into lines to find the line containing "Final Score"
    final_score_line = [line for line in lines if "Final Score" in line][0]
    score = float(final_score_line.split(":")[1].strip())
    
    results.append({
    "query": query,
    "type": row["type"],
    "intent": row.get("intent", "unknown"),
    "response": response,
    "evaluation": evaluation,
    "score": score
    })

# Convert to DataFrame
results_df = pd.DataFrame(results)

# Save results
results_df.to_csv("evaluation/results.csv", index=False)

print("\nPipeline execution completed. Results saved.")

print("\nAverage Score:", results_df["score"].mean())
print("Minimum Score:", results_df["score"].min())
print("Maximum Score:", results_df["score"].max())

results_df["type"] = df["type"]

print("\nAverage Score by Type:")
print(results_df.groupby("type")["score"].mean())

print("\nCoverage by Intent:")
print(results_df.groupby("intent")["score"].count())

print("\nDetailed Results:")
print(results_df[["query", "type", "intent", "score"]])
print("\nOverall Average Score:", results_df["score"].mean())
print("\nAverage Score by Type:")
print(results_df.groupby("type")["score"].mean())
print("\nAverage Score by Intent:")
print(results_df.groupby("intent")["score"].mean())

# Identify Worst Cases
print("\nLowest Scoring Cases:")
print(results_df.sort_values(by="score").head(5))

# Run Pipeline
# python -m evaluation.run_pipeline