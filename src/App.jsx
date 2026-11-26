
import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import Login from './pages/login'
import Projects from './pages/project'
import Tasks from './pages/tasks'
import Team from './pages/team'
import Settings from './pages/settings'
import Dashboard from './pages/dashboard'
import Clients from './pages/clients'
import Calender from './pages/calender'
import Register from './pages/register'

import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  
  const handlesubmit=(event)=>{
    event.preventDefault();
    console.log(email,password)
  }

  function print(){
  console.log("Printing statements")
  console.log(email,password)
}

  return (
    <>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/project" element={<Projects />} />
      <Route path="/tasks" element={<Tasks/>} />
      <Route path="/team" element={<Team/>}/>
      <Route path="/settings" element={<Settings/>} />
      <Route path="/Dashboard" element={<Dashboard/>}/>
      <Route path="/Clients" element={<Clients/>}/>
      <Route path="/calender" element={<Calender/>}/>
      <Route path="/register" element={<Register/>}/>
        </Routes>
        </BrowserRouter>
    {/*
      <>
    <div className="text-blue-500">HI</div>
    <div className="email">Email</div>
    <input type="email" required placeholder="Enter your email" value={email} onChange={(e)=> setEmail(e.target.value)} /><br/><br/>
    <div className="password">Password</div>
    <input type="password" required placeholder="Enter your password" value={password} onChange={(e)=> setPassword(e.target.value)}/>
    <button type="submit" onClick={()=>console.log(email,password)}>Submit</button><br/><br/>
    <button type="submit" onClick={()=>print()}>Submit</button>
    

    <form action="" onSubmit={handlesubmit}>
       <input type="email" required placeholder="Enter your email" value={email} onChange={(e)=> setEmail(e.target.value)} /><br/><br/>
    
    <input type="password" required placeholder="Enter your password" value={password} onChange={(e)=> setPassword(e.target.value)}/>
    
    <button type="submit">Submit</button>
    </form>

 

  </>
  */} 
    </>
  )
}

export default App
