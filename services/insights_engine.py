from openai import AzureOpenAI
import os
import time
from services.langfuse_tracker import trace_llm_call


def _get_chat_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_CHAT_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_CHAT_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_CHAT_ENDPOINT"),
    )


def generate_insights(df):
    client = _get_chat_client()
    model = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4.1")

    summary = df.describe(include="all").to_string()
    columns_info = df.dtypes.to_string()
    sample = df.head(5).to_string()

    prompt = f"""
    You are an expert data analyst. Analyze the following dataset and provide structured, actionable insights.

    ## Dataset Info
    **Columns and Types:**
    {columns_info}

    **Statistical Summary:**
    {summary}

    **Sample Data:**
    {sample}

    ## Instructions
    Provide your analysis in the following format:

    1. **Key Observations** - 3-5 main patterns or notable findings
    2. **Data Quality Notes** - any issues like missing values, outliers, or inconsistencies
    3. **Actionable Recommendations** - 2-3 specific suggestions based on the data
    4. **Interesting Correlations** - any relationships between columns worth exploring

    Use markdown formatting for readability."""

    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert data analyst who provides clear, actionable insights from datasets.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1500,
    )
    elapsed = time.time() - start_time

    output = response.choices[0].message.content

    trace_llm_call(
        name="generate_insights",
        input_text=prompt,
        output_text=output,
        model=model,
        metadata={
            "rows": df.shape[0],
            "columns": df.shape[1],
            "elapsed_seconds": round(elapsed, 2),
            "tokens_used": response.usage.total_tokens if response.usage else None,
        },
    )

    return output
