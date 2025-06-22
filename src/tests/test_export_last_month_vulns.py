import os
import builtins
import pytest
from unittest.mock import patch, Mock

@patch("requests.post")
@patch("requests.get")
def test_export_last_month_vulns(mock_get, mock_post):
    # Fake download content
    fake_csv = b"pluginID,cve,ip\n19506,CVE-1999-0001,192.168.1.1"

    # Mock POST to initiate export
    mock_post.return_value = Mock(status_code=200)
    mock_post.return_value.json.return_value = {"file": 1234}

    # Mock GET to download file
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.content = fake_csv

    # Import the real script (inside src)
    import src.export_last_month_vulns as mod

    # Mock open to avoid actually writing the file (except for verification)
    output_path = "exported_vulns.csv"

    if os.path.exists(output_path):
        os.remove(output_path)

    mod.export_vulnerabilities()

    # Assert file was created
    assert os.path.exists(output_path)

    with open(output_path, "rb") as f:
        content = f.read()
    assert b"pluginID" in content
    assert b"CVE-1999-0001" in content
    assert b"192.168.1.1" in content

    # Cleanup
    os.remove(output_path)
