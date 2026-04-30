from openai import AzureOpenAI
import os
import time
import pandas as pd
from services.langfuse_tracker import trace_llm_call


def _get_chat_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_CHAT_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_CHAT_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_CHAT_ENDPOINT"),
    )


def run_nl_query(df, question):
    """Translate a natural-language question into a pandas expression, execute it, and return the result."""
    client = _get_chat_client()
    model = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4.1")

    schema = df.dtypes.to_string()
    sample = df.head(3).to_string()
    columns = list(df.columns)

    prompt = f"""You are a pandas expert. Given a DataFrame `df` with these columns and types:
{schema}

Column names: {columns}

Sample data:
{sample}

The user asks: "{question}"

Return ONLY a single valid Python pandas expression that answers the question.
Rules:
- The DataFrame variable is called `df`.
- You may use `pd` (pandas) in the expression.
- Return ONLY the expression, nothing else. No markdown, no explanation, no code fences.
- The expression must be a single line that evaluates to a result.
- For date filtering, use pd.to_datetime() to convert columns first if needed.
- If counting, use .shape[0] or .count() or len() as appropriate.
- If summing, use .sum(). If averaging, use .mean()."""

    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a pandas code generator. Return ONLY a single executable pandas expression. No markdown, no explanation.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=300,
    )
    elapsed = time.time() - start_time

    code = response.choices[0].message.content.strip()
    if code.startswith("```"):
        code = code.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

    trace_llm_call(
        name="nl_query",
        input_text=question,
        output_text=code,
        model=model,
        metadata={
            "rows": df.shape[0],
            "columns": df.shape[1],
            "elapsed_seconds": round(elapsed, 2),
            "tokens_used": response.usage.total_tokens if response.usage else None,
        },
    )

    try:
        result = eval(code, {"__builtins__": {}}, {"df": df, "pd": pd})
        if isinstance(result, (pd.DataFrame, pd.Series)):
            answer = result
        else:
            answer = str(result)
        return {"answer": answer, "code": code, "error": None}
    except Exception as e:
        return {"answer": None, "code": code, "error": str(e)}
