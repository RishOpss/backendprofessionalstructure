# productionbackend

<!-- Written by Euron Code project setup. Run /init to let the model fill in the details. -->

Stack: Python, FastAPI

## Commands
- `pip install -e .`

## Layout
```
app/  (14 files)
  Dockerfile
  api/
  background_task/
  core/
  dependencies/
  main.py
  middleware/
  repository/
  requirements.txt
  schemas/
  services/
src/  (1 files)
  productionbackend/
FLOW.md
FLOW.pdf
pyproject.toml
README.md
uv.lock
```

Entry points: app/main.py, script: productionbackend = "productionbackend:main"

## Conventions
- (add the conventions of this project here)
