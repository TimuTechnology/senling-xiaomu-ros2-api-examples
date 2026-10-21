import cv2
import sounddevice as sd
import pyaudio
import wave
import time
import threading

# ==============================================================================
# IMPORTANT INSTRUCTIONS BEFORE RUNNING:
# 1. You MUST stop the default XiaoMu processes first to avoid hardware conflicts.
#    Run the following commands in your terminal:
#    sudo pkill -f robot_listener
#    sudo pkill -f robot_speaker
#    sudo pkill -f robot_eye
#
# 2. Run this test script using sudo:
#    sudo python3 hardware_raw_demo.py
# ==============================================================================

def camera_worker():
    print("[Camera] Starting...")
    # Open the camera device (usually index 0)
    cap = cv2.VideoCapture(0)
    # Set MJPG format to ensure high frame rate
    cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    
    if not cap.isOpened():
        print("[Camera] Error: Cannot open camera.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 'frame' is a raw BGR NumPy array.
            # TODO: Encode the frame (e.g., to JPEG) and send it to Windows via TCP/WebSocket.
            
            # Brief sleep to reduce CPU usage
            time.sleep(0.03) 
    except Exception as e:
        print(f"[Camera] Error: {e}")
    finally:
        cap.release()
        print("[Camera] Stopped.")

# ==========================================
# 2. Raw Microphone Hardware Access
# ==========================================
def audio_callback(indata, frames, time_info, status):
    if status:
        print(f"[Mic] Status: {status}")
        
    # 'indata' contains raw int16 PCM audio data.
    # TODO: Send indata.tobytes() to Windows via TCP/WebSocket.
    pass

def microphone_worker():
    print("[Mic] Starting...")
    SAMPLERATE = 16000
    CHANNELS = 1
    BLOCKSIZE = 2048

    try:
        # Use RawInputStream to capture the lowest-level data
        with sd.RawInputStream(device=0, samplerate=SAMPLERATE, 
                               blocksize=BLOCKSIZE, dtype="int16", 
                               channels=CHANNELS, callback=audio_callback):
            while True:
                sd.sleep(1000) # Keep the thread alive
    except Exception as e:
        print(f"[Mic] Error: {e}")
    finally:
        print("[Mic] Stopped.")

# ==========================================
# 3. Raw Speaker Hardware Access (Playback)
# ==========================================
def speaker_worker(wav_file_path):
    print(f"[Speaker] Will play: {wav_file_path}")
    time.sleep(5) # Wait a bit to ensure other threads have started
    
    p = pyaudio.PyAudio()
    try:
        wf = wave.open(wav_file_path, 'rb')
        stream = p.open(
            format=pyaudio.paInt16,
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            frames_per_buffer=1024,
            output=True
        )

        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()
        wf.close()
        print("[Speaker] Playback finished.")
    except Exception as e:
        print(f"[Speaker] Error: {e}")
    finally:
        p.terminate()

# ==========================================
# Main: Run all hardware threads concurrently
# ==========================================
if __name__ == "__main__":
    print("Starting Hardware Demo... Press Ctrl+C to stop.")
    
    # Replace this with an actual .wav file path on the robot
    TEST_WAV = "/root/asset/audio/welcome.wav" 

    # Create threads
    t_cam = threading.Thread(target=camera_worker, daemon=True)
    t_mic = threading.Thread(target=microphone_worker, daemon=True)
    # Run the speaker in a thread to prevent blocking
    t_spk = threading.Thread(target=speaker_worker, args=(TEST_WAV,), daemon=True)

    # Start threads
    t_cam.start()
    t_mic.start()
    t_spk.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
