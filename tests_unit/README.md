#### Usage:

Requirements: [pytest](https://docs.pytest.org/en/latest/)
  
Run tests: `pytest -v test_github_units.py`

File [github_responses.json](github_responses.json) contains serialized json github responses, which are used for mocking in tests


To update mock data run [mock_github_responses.py](mock_github_responses.py),
but it is not necessary to do it very frequently. Only if format of original responses could be changed.  
After refreshing mock data there might be need to adjust values in [expected_app_responses.py](expected_app_responses.py) 
