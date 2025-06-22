from unittest.mock import patch, Mock

@patch("requests.post")
@patch("requests.get")
def test_export_last_month_vulns(mock_get, mock_post, tmp_path):
    # Fake download content
    fake_csv = b"pluginID,cve,ip\n19506,CVE-1999-0001,192.168.1.1"

    # Mock POST to initiate export
    mock_post.return_value = Mock(status_code=200)
    mock_post.return_value.json.return_value = {"file": 1234}

    # Mock GET to download file
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.content = fake_csv

    # Patch the output filename to use a temp file
    output_file = tmp_path / "exported_vulns.csv"

    # ✅ Importa el módulo UNA SOLA VEZ (aquí es suficiente)
    import src.export_last_month_vulns as mod

    # Patch the open to write to temp file instead
    original_open = open
    def open_patch(path, *args, **kwargs):
        if path == "exported_vulns.csv":
            return original_open(output_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)

    with patch("builtins.open", new=open_patch):
        mod.export_vulnerabilities()

    # Assertions
    assert output_file.exists()
    content = output_file.read_bytes()
    assert b"pluginID" in content
    assert b"CVE-1999-0001" in content
    assert b"192.168.1.1" in content
