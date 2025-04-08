def clean_code(response_text: str):
    response_text = response_text.strip()
    
    parts = response_text.split("```")
    if len(parts) > 1:
        response_text = parts[1].strip()
    
    if response_text.lower().startswith("python"):
        response_text = response_text.split("\n", 1)[-1].strip()
    
    if "Note that" in response_text:
        response_text = response_text.split("Note that", 1)[0].strip()
    
    response_text = response_text.replace("```", "").strip()
    
    return response_text