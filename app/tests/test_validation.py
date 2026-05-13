from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


ACCEPTED_DIR = Path("tests/images/accepted")
REJECTED_DIR = Path("tests/images/rejected")


def validate_image(image_path):
    with open(image_path, "rb") as image_file:
        response = client.post(
            "/validate",
            files={
                "file": (
                    image_path.name,
                    image_file,
                    "image/jpeg"
                )
            }
        )

    assert response.status_code == 200

    return response.json()


def test_accepted_images():
    for image_path in ACCEPTED_DIR.glob("*"):
        result = validate_image(image_path)

        assert result["approved"] is True, (
            f"Expected approved image: "
            f"{image_path.name}"
        )


def test_rejected_images():
    for image_path in REJECTED_DIR.glob("*"):
        result = validate_image(image_path)

        assert result["approved"] is False, (
            f"Expected rejected image: "
            f"{image_path.name}"
        )