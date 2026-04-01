import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [reactCode, setReactCode] = useState('// Your converted React code will appear here...')
  const [isLoading, setIsLoading] = useState(false)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleConvert = async () => {
    if (!file) {
      alert("Please upload an HTML file first!")
      return
    }

    setIsLoading(true)
    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch("http://127.0.0.1:8000/convert", {
        method: "POST",
        body: formData
      })
      const data = await res.json()
      setReactCode(data.react_code)
    } catch (error) {
      setReactCode("// Error connecting to the backend. Is FastAPI running?")
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(reactCode)
    alert("Code copied to clipboard! 🚀")
  }

  return (
    <div className="app-container">
      <header className="navbar">
        <h1>🔥 CodeMorph AI <span className="badge">V1.5</span></h1>
        <p>Frontend Engine Laboratory</p>
      </header>

      <main className="dashboard">
        {/* LEFT PANEL: Controls */}
        <div className="panel control-panel">
          <h2>Input</h2>
          <div className="upload-box">
            <input type="file" accept=".html" onChange={handleFileChange} />
            {file && <p className="file-name">Selected: {file.name}</p>}
          </div>
          
          <button 
            className="convert-btn" 
            onClick={handleConvert}
            disabled={isLoading}
          >
            {isLoading ? "Morphing..." : "Convert to React"}
          </button>
        </div>

        {/* RIGHT PANEL: Output */}
        <div className="panel output-panel">
          <div className="output-header">
            <h2>Output</h2>
            <button className="copy-btn" onClick={handleCopy}>Copy Code</button>
          </div>
          <div className="code-window">
            <pre className="code-block">
              <code>{reactCode}</code>
            </pre>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App