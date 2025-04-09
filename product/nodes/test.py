from config.groq import groqClients

def check_api_key_status(client, index):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "hello"}]
        )
        return {f"api_key_{index + 1}": "working"}
    except Exception as e:
        return {f"api_key_{index + 1}": "not_working", "error": str(e)}

def check_api_keys():
    output = []
    for i, client in enumerate(groqClients):
        output.append(check_api_key_status(client, i))
    return output