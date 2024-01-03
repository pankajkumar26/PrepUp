import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="container">
        <h1>Prep - Up</h1>
        <h3>Platform for Communication, Preparation and Generation</h3>
        <div className="container">
          <div className="tiles">
            <a href="http://localhost:3001/"><div id="tile4" className="tile"><span className="tile-title">Chat with PDF</span></div></a>
            <a href="http://localhost:5174/"><div id="tile1" className="tile"><span className="tile-title">Text Summarizer</span></div></a>
            <a href="http://localhost:3000/"><div id="tile2" className="tile"><span className="tile-title">Article Generator</span></div></a>
            <a href="http://localhost:8501/"><div id="tile3" className="tile"><span className="tile-title">Interview Prep</span></div></a>
          </div>
        </div>
      </div>
    </>
  )
}

export default App
