%%writefile model_api.py
import google.generativeai as genai
import os

def query_model(prompt):
    try:

        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)


        available_models =[
            m.name.replace("models/", "")
            for m in genai.list_models()
            if 'generateContent' in m.supported_generation_methods
        ]

        if not available_models:
            return "Error: No text generation models are enabled for your API key."


        selected_model = available_models[0]
        for m in available_models:
            if "flash" in m:
                selected_model = m
                break

        model = genai.GenerativeModel(selected_model)

        response = model.generate_content(
            f"You are a professional fitness trainer. Output ONLY the requested markdown.\n\n{prompt}"
        )

        return response.text

    except Exception as e:
        return f"API Error: {str(e)}"
