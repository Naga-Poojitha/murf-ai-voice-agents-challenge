# Day 01 — Starter Voice Agent (Best version)

## What this does
- Starts a Flask server with a `/speak` endpoint that streams text-to-speech using **Murf Falcon** (streaming PCM) and plays audio locally.
- Also synthesizes and saves an MP3 `day1_output.mp3` for demo/upload.

## Setup (Windows / macOS / Linux)
1. Clone this repo and open the `day01` folder.
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Install requirements:
```
pip install -r requirements.txt
```
4. Create a `.env` file and set your key (or export env var):
```
MURF_API_KEY=your_real_murf_api_key_here
```
5. Run the app:
```
python app.py
```

## Test the agent
In another terminal run:

```
curl -X POST http://localhost:5000/speak -H "Content-Type: application/json" -d "{\"text\":\"Hello, this is Day 1 of the Murf AI Voice Agents Challenge.\"}"
```

This will start streaming audio to your speakers and save `day1_output.mp3` in the folder.

## Download
To download the generated MP3 (for uploading to LinkedIn):
```
curl http://localhost:5000/download --output day1_output.mp3
```

## Notes & Troubleshooting
- PyAudio: On Windows you may need the prebuilt wheel or `pip install pipwin` then `pipwin install pyaudio`.
- If streaming fails (network/permissions), the code falls back to synthesize an MP3 file.

## Demo image (Discord screenshot)
You can include this screenshot in your README or LinkedIn post. Local path (uploaded by you):
`/mnt/data/c3845e5f-9360-4b27-909f-890121b7d4bf.png`

Include it in README by uploading that image to the GitHub repo or hosting it — for your immediate demo you can reference it in the repo README.
