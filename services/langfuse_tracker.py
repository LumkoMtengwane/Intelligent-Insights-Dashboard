from langfuse import Langfuse
import os

_langfuse_client = None


def get_langfuse():
    global _langfuse_client
    if _langfuse_client is None:
        _langfuse_client = Langfuse(
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            host=os.getenv("LANGFUSE_HOST"),
        )
    return _langfuse_client


def trace_llm_call(name, input_text, output_text, model, metadata=None):
    """Log an LLM interaction to Langfuse with full metadata."""
    try:
        langfuse = get_langfuse()
        trace = langfuse.trace(name=name, metadata=metadata or {})
        trace.generation(
            name=name,
            model=model,
            input=input_text,
            output=output_text,
            metadata=metadata or {},
        )
        langfuse.flush()
    except Exception:
        pass
