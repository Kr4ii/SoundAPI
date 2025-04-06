# Check invalid formats
def test_invalid_file_format():
    response = client.post("/api/v1/process-audio/", 
        files={"file": ("test.txt", b"invalid", "text/plain")})
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

# Check audio processing
def test_valid_audio_processing():
    with open("tests/test_audio.wav", "rb") as f:
        response = client.post("/api/v1/process-audio/", 
            files={"file": ("test_audio.wav", f, "audio/wav")})
    assert response.status_code == 200
    assert "processed_file" in response.json()