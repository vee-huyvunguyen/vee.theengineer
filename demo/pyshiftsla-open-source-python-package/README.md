# pyshifsla
*You can watch the [video demo](https:/loom.com)
- What problems does this project solve ?
    - Calculating the SLA (service level agreement) of the customer support team. While ...
    - ... Minimizing API calls to the employees' timekeeping database
- How does the project solve the problems?
    - It is python package (you can install with `pip install pyshiftsla`)
    - That can logically generate employees' timekeeping (workshifts).
    - Then calculate employees' SLA, based on the generated workshifts.
- What skills do I want to show?:
    - The domain knowledge:
        - Customer services' SLA.
        - Human resource management.
    - The tools: python, bash, poetry, pydantic, PyPi(python package index), Github Actions
    - The techniques: OOP, Unit testing, CICD pipelines

# Steps to run the demo
## Option 1: With [uv](https://docs.astral.sh/uv/)
- Step 1: Install [uv](https://docs.astral.sh/uv/)
- Step 2: execute `uv sync`
- You Run any python file with `uv run python-file.py` at the top level of the project.
    - E.g.: `uv run steps/generate_employee_workshift.py`

## Option 2: Without [uv](https://docs.astral.sh/uv/)
- Step 1: Install the neede environment:
    - The project is tested with `python==3.10`, so you should install that version.
    - Install the dependencies in `requirements.txt`: `pip install -r requirements.txt`
- Run the python files:
    - E.g.: `uv run steps/generate_employee_workshift.py`


# References
- [The pyshiftsla project](https://pypi.org/project/pyshiftsla/)
