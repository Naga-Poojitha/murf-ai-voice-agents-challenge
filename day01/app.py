# app.py — Day 1 BEST starter voice agent
# Features:
# - Flask server with /speak endpoint
# - Uses Murf Falcon streaming TTS (PCM)
# - Plays audio locally using PyAudio
# - Saves an MP3 file for demo

import os
import threading
from flask import Flask, request, jsonify, send_file
from murf import Murf, MurfRegion
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MURF_API_KEY")
if not API_KEY:
    raise RuntimeError("Set MURF_API_KEY in your environment or .env file")

client = Murf(api_key=API_KEY, region=MurfRegion.GLOBAL)

app = Flask(__name__)

# -----------------------------
# PLAY PCM STREAM
# -----------------------------
def play_pcm_stream(pcm_generator, sample_rate=24000):
    import pyaudio
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        output=True
    )
    try:
        for chunk in pcm_generator:
            if chunk:
                stream.write(chunk)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

# -----------------------------
# STREAM + SAVE MP3
# -----------------------------
def stream_and_save(text, voice_id="Matthew", out_mp3="day1_output.mp3"):
    # Try low-latency streaming
    try:
        pcm_stream = client.text_to_speech.stream(
            text=text,
            voice_id=voice_id,
            model="FALCON",
            sample_rate=24000,
            format="PCM"
        )
        play_pcm_stream(pcm_stream, sample_rate=24000)
    except Exception as e:
        print("Streaming failed, falling back to synthesize():", e)

    # Always create demo MP3
    try:
        mp3_bytes = client.text_to_speech.synthesize(
            text=text,
            voice_id=voice_id,
            model="FALCON",
            format="mp3"
        )
        with open(out_mp3, "wb") as f:
            f.write(mp3_bytes)
    except Exception as e:
        print("MP3 synth failed:", e)

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    voice_id = data.get("voice_id", "Matthew")

    if not text:
        return jsonify({"error": "no text provided"}), 400

    t = threading.Thread(target=stream_and_save, args=(text, voice_id))
    t.start()

    return jsonify({
        "status": "processing",
        "message": "Audio streaming started. MP3 will be saved as day1_output.mp3"
    })

@app.route("/download", methods=["GET"])
def download():
    mp3_file = "day1_output.mp3"
    if not os.path.exists(mp3_file):
        return jsonify({"error": "No MP3 generated yet"}), 404
    return send_file(mp3_file, mimetype="audio/mpeg", as_attachment=True)

# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
