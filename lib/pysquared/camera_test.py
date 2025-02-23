import pytest
from unittest.mock import MagicMock, patch
import os

from camera_test import Sp_Camera

@pytest.fixture
def mock_camera():
    """Fixture to create a mocked Sp_Camera instance with dependencies mocked."""
    with patch("your_module.sdioio.SDCard") as mock_sdcard, \
         patch("your_module.storage.VfsFat") as mock_vfsfat, \
         patch("your_module.storage.mount"), \
         patch("your_module.camera.Camera") as mock_camera:
        
        # Mock the Camera instance
        mock_cam_instance = mock_camera.return_value
        mock_cam_instance.take_picture.return_value = 512 * 1024  # Simulate image size

        # Return the initialized Sp_Camera instance
        return Sp_Camera()


def test_take_picture(mock_camera, tmp_path):
    """Test take_picture() method"""
    # Patch 'open' to prevent actual file creation
    with patch("builtins.open", create=True) as mock_open:
        file_mock = MagicMock()
        mock_open.return_value = file_mock  # Simulate file object

        mock_camera.take_picture("test_image")

        # Ensure camera.take_picture() was called
        mock_camera.cam.take_picture.assert_called_once()

        # Ensure file write happened
        file_mock.write.assert_called()


def test_delete_picture(mock_camera, tmp_path):
    """Test delete_picture() method"""
    file_path = tmp_path / "test_image.jpg"

    # Simulate file creation
    file_path.write_text("fake_image_data")

    # Patch os.path.exists and os.remove
    with patch("os.path.exists", return_value=True), patch("os.remove") as mock_remove:
        result = mock_camera.delete_picture("test_image.jpg")
        assert result == 1
        mock_remove.assert_called_with("/sd/test_image.jpg")

    # Test deleting a non-existent file
    with patch("os.path.exists", return_value=False):
        result = mock_camera.delete_picture("non_existent.jpg")
        assert result == -1  # Should return -1 if file does not exist


def test_delete_picture_no_filename(mock_camera):
    """Ensure delete_picture() returns -1 when no filename is given"""
    result = mock_camera.delete_picture("")
    assert result == -1

