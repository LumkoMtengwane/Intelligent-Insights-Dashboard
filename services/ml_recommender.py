from openai import AzureOpenAI
import os
import time
import json
from services.langfuse_tracker import trace_llm_call


def detect_task_type(df, target_col=None):
    """Rule-based ML task detection: classification, regression, or clustering."""
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    n_samples = df.shape[0]
    n_features = df.shape[1] - (1 if target_col else 0)

    if target_col is None:
        return {
            "task_type": "clustering",
            "target": None,
            "n_features": n_features,
            "n_samples": n_samples,
            "reason": "No target column specified -- unsupervised analysis recommended.",
        }

    if target_col in categorical_cols:
        return {
            "task_type": "classification",
            "target": target_col,
            "n_classes": df[target_col].nunique(),
            "n_features": n_features,
            "n_samples": n_samples,
            "reason": f"Target '{target_col}' is categorical with {df[target_col].nunique()} classes.",
        }

    if target_col in numeric_cols:
        n_unique = df[target_col].nunique()
        ratio = n_unique / n_samples if n_samples > 0 else 0
        if n_unique <= 20 or ratio < 0.05:
            return {
                "task_type": "classification",
                "target": target_col,
                "n_classes": n_unique,
                "n_features": n_features,
                "n_samples": n_samples,
                "reason": f"Target '{target_col}' is numeric but has only {n_unique} unique values -- likely categorical.",
            }
        return {
            "task_type": "regression",
            "target": target_col,
            "n_features": n_features,
            "n_samples": n_samples,
            "reason": f"Target '{target_col}' is continuous numeric with {n_unique} unique values.",
        }

    return {
        "task_type": "clustering",
        "target": None,
        "n_features": n_features,
        "n_samples": n_samples,
        "reason": f"Column '{target_col}' not recognized -- defaulting to unsupervised.",
    }


def _get_chat_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_CHAT_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_CHAT_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_CHAT_ENDPOINT"),
    )


def suggest_models(df, task_info):
    """Use LLM to recommend top 3 ML models based on the dataset profile and task type."""
    client = _get_chat_client()
    model = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4.1")

    dtypes_str = df.dtypes.to_string()
    skew_str = df.select_dtypes(include=["number"]).skew().round(2).to_string()

    prompt = f"""You are an ML engineering advisor. Based on the following dataset profile, recommend the top 3 machine learning models.

## Task Info
- Task type: {task_info['task_type']}
- Target column: {task_info.get('target', 'None')}
- Number of features: {task_info['n_features']}
- Number of samples: {task_info['n_samples']}
- Reason: {task_info['reason']}

## Dataset Profile
- Shape: {df.shape}
- Column types:
{dtypes_str}
- Skewness of numeric columns:
{skew_str}
- Missing values: {df.isnull().sum().sum()} total

## Instructions
Return ONLY a valid JSON array with exactly 3 objects, each having:
- "name": model name (e.g., "Random Forest Classifier")
- "why": one sentence explaining why this model fits
- "hyperparameters": key hyperparameters to tune (as a short string)
- "considerations": performance or data considerations (one sentence)

Return raw JSON only. No markdown, no code fences."""

    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an ML advisor. Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=800,
    )
    elapsed = time.time() - start_time

    output = response.choices[0].message.content.strip()

    trace_llm_call(
        name="ml_suggest_models",
        input_text=prompt,
        output_text=output,
        model=model,
        metadata={
            "task_type": task_info["task_type"],
            "elapsed_seconds": round(elapsed, 2),
            "tokens_used": response.usage.total_tokens if response.usage else None,
        },
    )

    if output.startswith("```"):
        output = output.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

    try:
        models = json.loads(output)
        return models[:3]
    except json.JSONDecodeError:
        return [{"name": "Error", "why": "Could not parse model suggestions.", "hyperparameters": "", "considerations": output}]
