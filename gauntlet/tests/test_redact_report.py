import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "redact-report.py"
redact = runpy.run_path(str(SCRIPT))["redact"]
REQUEST_ID = "12345678-1234-1234-1234-123456789abc"


class RedactReportTests(unittest.TestCase):
    def test_prefixed_environment_keys(self):
        for key in ("EXAMPLE_API_KEY", "DB_PASSWORD", "SERVICE_TOKEN", "AWS_SECRET_ACCESS_KEY"):
            with self.subTest(key=key):
                self.assertEqual(redact(f"{key}=demo-secret\n"), f"{key}=[REDACTED]\n")
        self.assertEqual(
            redact("  export DB_PASSWORD='demo secret'\n"),
            "  export DB_PASSWORD=[REDACTED]\n",
        )

    def test_json_credentials_preserve_other_fields_and_structure(self):
        source = {
            "password": 'demo "quoted" \\ secret\nsecond line',
            "nested": [{"EXAMPLE_API_KEY": "demo-key", "request_id": REQUEST_ID}],
            "token_count": 12,
            "message": 'the word "password" is not a credential',
        }
        expected = {
            **source,
            "password": "[REDACTED]",
            "nested": [{"EXAMPLE_API_KEY": "[REDACTED]", "request_id": REQUEST_ID}],
        }
        for indent in (None, 2):
            with self.subTest(indent=indent):
                self.assertEqual(json.loads(redact(json.dumps(source, indent=indent))), expected)

    def test_json_scalar_credentials(self):
        source = '{"password": 123456, "token": null, "secret": true, "attempts": 2}'
        self.assertEqual(
            json.loads(redact(source)),
            {"password": "[REDACTED]", "token": "[REDACTED]", "secret": "[REDACTED]", "attempts": 2},
        )

    def test_json_in_logs_and_escaped_key(self):
        source = 'INFO {"pass\\u0077ord": "demo-secret", "ok": true}\n'
        self.assertEqual(
            redact(source), 'INFO {"pass\\u0077ord": "[REDACTED]", "ok": true}\n'
        )

    def test_uuid_is_preserved_unless_it_is_a_credential(self):
        source = f"request_id={REQUEST_ID}\nTOKEN={REQUEST_ID}\n"
        self.assertEqual(redact(source), f"request_id={REQUEST_ID}\nTOKEN=[REDACTED]\n")

    def test_existing_credential_formats(self):
        source = "password: demo-secret\nAuthorization: Bearer demo.token-123\nkey sk-demo12345678\n"
        self.assertEqual(
            redact(source),
            "password: [REDACTED]\nAuthorization: Bearer [REDACTED]\nkey [REDACTED]\n",
        )

    def test_empty_value_does_not_consume_next_line(self):
        source = "token:\nrequest_id=trace-123\n"
        self.assertEqual(redact(source), source)

    def test_cli_stdin_and_file_output(self):
        source = '{"password": "demo-secret", "request_id": "trace-123"}\n'
        expected = '{"password": "[REDACTED]", "request_id": "trace-123"}\n'
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], input=source, text=True, capture_output=True, check=True
        )
        self.assertEqual(result.stdout, expected)
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.json"
            output_path = Path(directory) / "output" / "report.json"
            input_path.write_text(source, encoding="utf-8")
            subprocess.run(
                [sys.executable, str(SCRIPT), str(input_path), "-o", str(output_path)],
                capture_output=True, text=True, check=True,
            )
            self.assertEqual(output_path.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
