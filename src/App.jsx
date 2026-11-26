
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Login from './pages/login';
import Project from './pages/project';
import Task from './pages/tasks';
import Calender from './pages/Calender';
import Clients from './pages/Clients';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import Team from './pages/Team';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/project" element={<Project />} />
        <Route path="/task" element={<Task />} />
        <Route path= "/Calender" element = {<Calender/>}/>
        <Route path= "/Clients" element = {<Clients/>}/>
        <Route path= "/Dashboard" element = {<Dashboard/>}/>
        <Route path= "/Settings" element = {<Settings/>}/>
        <Route path= "/Team" element = {<Team/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
