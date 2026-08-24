# Test and Reporting Commands

সব commands project root থেকে Git Bash-এ চালাতে হবে।

## Project Setup

নতুন Git Bash session খোলার পর virtual environment activate করতে:

```bash
source .venv/Scripts/activate
```

প্রথমবার project setup করার সময় অথবা `requirements.txt` পরিবর্তনের পর dependencies install করতে:

```bash
python -m pip install -r requirements.txt
```

প্রথম setup অথবা Playwright version update করার পর Chromium install করতে:

```bash
python -m playwright install chromium
```

নতুন direct dependency যোগ হলে সেটি exact versionসহ `requirements.txt`-এ রাখতে হবে। যেমন:

```text
package-name==x.y.z
```

## Test Run

Project-এর সব tests চালিয়ে full regression check করতে:

```bash
pytest -v
```

শুধু login feature-এর tests চালাতে:

```bash
pytest tests/test_login.py -v
```

শুধু successful-login testটি isolate করে চালাতে:

```bash
pytest tests/test_login.py::test_valid_user_can_log_in -v
```

Tests execute না করে pytest কোন tests collect করছে তা দেখতে:

```bash
pytest --collect-only -q
```

## Visual Debugging

Test চলার সময় browser interaction সরাসরি দেখতে:

```bash
pytest tests/test_login.py -v --headed
```

Playwright actions ধীরে দেখে temporary debugging করতে:

```bash
pytest tests/test_login.py -v --headed --slowmo=500
```

Slow motion শুধু debugging-এর জন্য। Regular test অথবা CI pipeline-এ এটি ব্যবহার করা হবে না।

## Test Reports

যেকোনো test run-এর result দেখতে HTML report খুলতে:

```bash
explorer.exe reports/report.html
```

python -c "from pathlib import Path; import webbrowser; webbrowser.open(Path('reports/report.html').resolve().as_uri())"

Assertion steps এবং failure details দেখতে sanitized execution log খুলতে:

```bash
cat reports/execution.log
```

CI-compatible raw test result দেখতে JUnit XML VS Code-এ খুলতে:

```bash
code reports/junit.xml
```

প্রতিটি test run-এর পরে automatically পাওয়া যাবে:

- `reports/report.html` — readable HTML report
- `reports/junit.xml` — CI-compatible result
- `reports/execution.log` — sanitized execution details
- `test-results/` — failure screenshots এবং traces

## Failure Investigation

Regular concise output-এ প্রয়োজনীয় detail পাওয়া না গেলে complete failure outputসহ login test চালাতে:

```bash
pytest tests/test_login.py -v --full-failure-output
```

Failure-এর সময় তৈরি হওয়া screenshots খুঁজতে:

```bash
find test-results -type f -name "*.png"
```

Detailed Playwright debugging-এর জন্য trace files খুঁজতে:

```bash
find test-results -type f -name "trace.zip"
```

পাওয়া trace file Trace Viewer-এ খুলতে, `<trace-path>`-এর জায়গায় real path দিতে হবে:

```bash
python -m playwright show-trace "<trace-path>"
```

`reports/` এবং `test-results/` sensitive এবং Git-ignored। এগুলো share করার আগে sensitive information আছে কিনা review করতে হবে।
