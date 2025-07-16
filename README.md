# Reddit User Persona Extractor

This project extracts a detailed user persona from a Reddit user's public posts and comments. It uses NLP and local LLMs to analyze interests, writing style, tone, demographics, values, goals, and challenges, and cites the posts/comments used for each insight.

## Features
- Input a Reddit user profile URL
- Scrapes recent posts and comments
- Builds a persona with:
  - Interests
  - Writing Style
  - Tone
  - Frequently Mentioned Topics
  - Demographics
  - Values
  - Goals
  - Challenges
- Cites each post/comment used for persona extraction
- Outputs the persona to a text file in the `output/` directory

## Technologies Used
- Python 3.10+
- [PRAW](https://praw.readthedocs.io/) (Reddit API)
- [spaCy](https://spacy.io/) (NER)
- [Hugging Face Transformers](https://huggingface.co/transformers/) (summarization, sentiment analysis)

## Setup Instructions

1. **Clone the repository:**
   ```bash
    git clone "https://github.com/Khushiii7/persona-scrapper.git"
    cd persona-scrapper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** If you encounter errors with NumPy or TensorFlow, ensure you are using `numpy<2`.

3. **(Optional) Download spaCy model:**
   If you haven't used spaCy before, run:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the script:**
   ```bash
   python main.py
   ```
   Enter a Reddit profile URL when prompted (e.g. `https://www.reddit.com/user/kojied/`).

5. **Output:**
   - The persona will be saved as `output/<username>_persona.txt`.

## Example
```
Enter Reddit Profile URL: https://www.reddit.com/user/kojied/
Persona for kojied saved successfully!
```

## Notes
- The script fetches up to 20 posts and 20 comments per user.
- All persona fields are supported by citations (links to posts/comments).
- If LLM models are not available, the script falls back to spaCy and heuristics.

## Troubleshooting
- If you see errors about NumPy or TensorFlow, run:
  ```bash
  pip install numpy<2
  ```
- If you see errors about missing spaCy models, run:
  ```bash
  python -m spacy download en_core_web_sm
  ```

## License
This project is for assignment/demo purposes only. 
