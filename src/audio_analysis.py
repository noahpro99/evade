import openai

from settings import settings


def analyze_text_for_threats(text: str) -> bool:
    if not settings.TOGETHER_API_KEY:
        print("Warning: TOGETHER_API_KEY not set, skipping AI analysis")
        return False

    try:
        client = openai.OpenAI(
            api_key=settings.TOGETHER_API_KEY,
            base_url="https://api.together.xyz/v1",
        )

        prompt = f"""Analyze the following text from a conversation. Does it indicate any suspicious threats, dangerous situations, or content that would warrant contacting authorities or third parties for safety concerns? Consider threats to personal safety, criminal activity, or emergency situations.

Text: "{text}"

Answer only 'YES' or 'NO'."""

        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.1,
        )

        content = response.choices[0].message.content
        assert isinstance(content, str)
        result = content.strip().upper()
        return "YES" in result

    except Exception as e:
        print(f"Error analyzing text with AI: {e}")
        return False
