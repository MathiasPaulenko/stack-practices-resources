# Test Double: Replace Dependencies with Stubs, Spies, Fakes

Runnable implementations of all five Meszaros test-double types — dummy, stub, spy, fake, mock — in pytest and jest.

## Files

- `test_doubles.py` — pytest examples: dummy logger, repository stub, MagicMock spy, in-memory fake repository, mock with exact-call verification.
- `test_doubles.test.js` — jest equivalents: `jest.fn()` stubs/spies, in-memory fake, mock verification.
- `package.json` — minimal jest setup.
- `pytest.ini` — test discovery config.

## Run

```bash
# Python
pip install pytest
pytest test_doubles.py

# JavaScript
npm install
npm test
```

Source article: https://stackpractices.com/patterns/test-double-pattern/
