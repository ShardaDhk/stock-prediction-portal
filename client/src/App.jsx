import { useState } from 'react'
import './assets/css/style.css'
import Header from './components/Header'
import Home from './components/Home'
import Footer from './components/Footer'
import Register from './components/Register'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './components/Login'
import AuthProvider from './AuthProvider'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <AuthProvider>
        <BrowserRouter>
        <Header />
          <Routes>
            <Route path='/' element={<Home />}/>
            <Route path='register/' element={<Register />} />
            <Route path='login/' element={<Login />}/>
          </Routes>
        <Footer />
        </BrowserRouter>
      </AuthProvider>
    </>
  )
}

export default App
