import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Load API KEY from Cohere AI
co = cohere.Client(os.getenv('AI_API_KEY'))

def generate_content(user):
    """Generates LinkedIn post content based on user topics."""
    prompt = f"{user.topics}"

    try:
        # Takes the response of the Pompt given
        response = co.generate(
            model = "command-r-plus",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.generations[0].text
    
    except Exception as e:
        print(f"Error generating LinkedIn post: {e}")
        return "Failed to generate content."