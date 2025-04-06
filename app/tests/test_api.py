import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

# fixture test audio
@pytest.fixture
def test_audio_wav():
    with open("tests/test_audio.wav", "rb") as f:
        yield f

@pytest.fixture
def test_audio_mp3():
    with open("tests/test_audio.mp3", "rb") as f:
        yield f

def test_noise_reduction_wav(test_audio_wav):
    response = client.post(
        "/api/v1/noise-reduction/",
        files={"file": ("test.wav", test_audio_wav, "audio/wav")},
        data={"reduction_strength": 0.5}
    )
    assert response.status_code == 200
    assert "processed_file" in response.json()
    assert response.json()["processed_file"].endswith(".wav")

def test_bandpass_filter_mp3(test_audio_mp3):
    response = client.post(
        "/api/v1/bandpass-filter/",
        files={"file": ("test.mp3", test_audio_mp3, "audio/mpeg")},
        data={"lowcut": 300, "highcut": 3400}
    )
    assert response.status_code == 200
    assert os.path.exists("data/output/" + response.json()["processed_file"].split("/")[-1])

def test_normalize_volume_invalid_format():
    response = client.post(
        "/api/v1/normalize-volume/",
        files={"file": ("test.txt", b"invalid", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

def test_processed_file_download(test_audio_wav):
    response = client.post(
        "/api/v1/normalize-volume/",
        files={"file": ("test.wav", test_audio_wav, "audio/wav")},
        data={"target_dBFS": -20.0}
    )
    file_url = response.json()["processed_file"]
    download_response = client.get(file_url)
    assert download_response.status_code == 200
    assert len(download_response.content) > 1024  # Check file size > 1KB