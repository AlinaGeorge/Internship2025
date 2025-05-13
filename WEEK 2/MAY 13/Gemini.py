api_key = 'AIzaSyBofgdJ1q3AwtSIIu9hhBssVXpgsE-Wh-0'

import google.generativeai as genai

# Configure the API key
genai.configure(api_key=api_key)

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

# 1. Text Generation
def generate_text(prompt):
    return model.generate_content(prompt)

# 2. Text Summarization
def summarize_text(text):
    return model.generate_content(f"Summarize the following text: {text}")

# Example usage
if __name__ == "__main__":
    prompt = "Tell me a short story about a robot and a cat."
    print("Generated Text:\n", generate_text(prompt).text)

    long_text = """
    Artificial intelligence is transforming industries from healthcare to finance. 
    It enables automation, insights, and better decision-making. Companies are 
    investing heavily in AI to streamline operations and improve user experiences.
    """
    print("\nSummary:\n", summarize_text(long_text).text)
