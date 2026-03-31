from fastapi import FastAPI, UploadFile, File
from parser import html_to_ui_tree
from generator_react import generate_react

app = FastAPI()


@app.get("/")
def home():
    return {"message": "CodeMorph AI running 🚀"}


@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    content = await file.read()
    html = content.decode("utf-8")

    ui_tree = html_to_ui_tree(html)
    react_body = generate_react(ui_tree, indent=1)

    react_code = f"""function App() {{
  return (
{react_body}  );
}}

export default App;
"""

    return {
        "filename": file.filename,
        "react_code": react_code,
    }
