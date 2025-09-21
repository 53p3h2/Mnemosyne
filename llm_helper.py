from ollama import chat

MODEL = 'qwen3:4b'

def generate_response(prompt):
    try:
        response = chat(model=MODEL, messages=[{'role': 'system', 'content': 'You are a helpful AI coach and gives short answers.'},
                                                      {'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)} - Try running 'ollama serve'."

def build_profile(answers):
    prompt = f"Based on these questionnaire answers: {json.dumps(answers)}, create a JSON profile with keys: goals (list), habits (list), motivations (string), challenges (list)."
    return json.loads(generate_response(prompt))  # Assume LLM outputs valid JSON; add parsing error handling if needed.

def generate_advice(profile, task_desc):
    prompt = f"User profile: {json.dumps(profile)}. Task: {task_desc}. Provide motivational advice, a plan, and inspiration tailored to their goals."
    return generate_response(prompt)

def generate_motivation(profile, task_desc):
    prompt = f"Motivate the user for '{task_desc}' based on profile: {json.dumps(profile)}. Keep it short and inspiring."
    return generate_response(prompt)

