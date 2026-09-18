# Navjeevan.AI

Navjeevan.AI is a Streamlit-based sustainability assistant that helps users analyze unwanted household items, identify the best circular economy option, and discover nearby donation or recycling opportunities.

The app uses image input and Google Gemini to assess an item's condition, suggest repair/reuse/upcycling paths, and provide a DIY blueprint for repurposing the item.

## Features

- Upload an image of an unwanted item
- Analyze item type, material, condition, and reuse potential
- Rank circular economy options such as repair, reuse, upcycle, donate, recycle, and dispose
- Suggest local NGO or donation partners based on the user’s location
- Generate a beginner-friendly DIY upcycling or reuse guide
- Provide a conversational sustainability assistant for follow-up questions
- Built with a clean, mobile-friendly Streamlit interface

## Tech Stack

- Python
- Streamlit
- Pillow
- Google Generative AI (Gemini)

## Requirements

Install the required Python packages:

```bash
pip install streamlit pillow google-generativeai
```

## Setup

1. Clone or open the project folder.
2. Make sure you have Python 3 installed.
3. Add your Google Gemini API key.

You can provide the key in two ways:

- Through the sidebar in the app UI
- Or as an environment variable named `GEMINI_API_KEY`

Example:

```bash
set GEMINI_API_KEY=your_api_key_here
```

On macOS/Linux:

```bash
export GEMINI_API_KEY=your_api_key_here
```

## Run the App

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal (usually http://localhost:8501).

## App Workflow

1. Upload a photo of the item.
2. Enter the city or region for NGO lookup.
3. Click the analysis button.
4. Review:
   - the full sustainability report
   - the DIY blueprint tab
   - local donation partner suggestions
   - the chat assistant for follow-up questions

## Notes

- The app is intended as a decision-support tool and should not replace professional judgment or local waste-management guidance.
- The app uses Google Gemini for AI-generated recommendations, which may require human verification before acting on real-world disposal, repair, or donation decisions.
- The NGO section is designed to provide broad guidance based on the user’s input and item type, but local availability may vary.

## Project Context

This project aligns with the sustainability theme of responsible consumption and production, focusing on extending the life cycle of everyday items through repair, reuse, and upcycling.
