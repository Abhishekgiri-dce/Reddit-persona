import praw
import os
import google.generativeai as genai

# Gemini API Key
genai.configure(api_key="AIzaSyAmlT4MkeD6CjRfVxAc5J-kxTCpMPAgntA")

# Reddit API setup
reddit = praw.Reddit(
    client_id='OneCqpSMKp8Iuj_AAPF--Q',
    client_secret='9ytt0p8vmJqC9gsj0LZjItE8cCy-Hw',
    user_agent='script by /u/OpenPossession5996'
)

# Fetch Reddit user data
def get_user_data(username):
    user = reddit.redditor(username)
    posts = []
    comments = []

    for i, submission in enumerate(user.submissions.new(limit=10), 1):
        posts.append(f"[Post #{i}] Title: {submission.title}\nText: {submission.selftext}")

    for i, comment in enumerate(user.comments.new(limit=20), 1):
        comments.append(f"[Comment #{i}] {comment.body}")

    return posts, comments

# Generate persona using Gemini
def generate_persona(posts, comments):
    post_text = "\n\n".join(posts)
    comment_text = "\n\n".join(comments)

    prompt = f"""
You are an AI user profiler. Based on the following Reddit user's posts and comments, generate a detailed user persona.

Include:
- Guessed Name
- Age group
- Personality traits
- Interests & hobbies
- Occupation guess (if possible)
- Writing/communication style
- At least 4-5 citations from their posts or comments that support your observations.

--- POSTS ---
{post_text}

--- COMMENTS ---
{comment_text}
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else str(response)

# Save output
def save_persona(username, persona):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{username}_persona.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(persona)
    print(f"\n
           Persona saved to: {filepath}")

#  Run the script
if __name__ == "__main__":
    url = input("Enter Reddit profile URL: ").strip()
    username = url.split("/")[-2]
    print(f"\n Fetching data for Reddit user: {username}...")
    posts, comments = get_user_data(username)
    print("\n Generating user persona using Gemini...")
    persona = generate_persona(posts, comments)
    print("\n USER PERSONA:\n")
    print(persona)
    save_persona(username, persona)
