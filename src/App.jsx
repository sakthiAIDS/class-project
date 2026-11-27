import { BrowserRouter, Routes, Route } from "react-router-dom";

<<<<<<< HEAD
import Login from "./pages/login";
import Projects from "./pages/project";
import Tasks from "./pages/tasks";
import Team from "./pages/team";
import Settings from "./pages/settings";
import Dashboard from "./pages/dashboard";
import Clients from "./pages/clients";
import Calender from "./pages/calender";
import Register from "./pages/register";

import Admin from "./pages/Admin/adminlayout";
import Admindashboard from "./pages/Admin/dashboard";
import Adminsettings from "./pages/Admin/settings";
import Userdetails from "./pages/Admin/userDetails";

import "./App.css";
=======
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
>>>>>>> f251ae727b99e3648c34b19e63e07930c693c0f0

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
<<<<<<< HEAD
        <Route path="/projects" element={<Projects />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/team" element={<Team />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/clients" element={<Clients />} />
        <Route path="/calender" element={<Calender />} />
        <Route path="/register" element={<Register />} />

        <Route path="/admin" element={<Admin />}>
          <Route
            path="admindashboard"
            element={<Admindashboard />}
          />
          <Route
            path="settings"
            element={<Adminsettings />}
          />
          <Route
            path="userdetails"
            element={<Userdetails />}
          />
        </Route>

=======
        <Route path="/project" element={<Project />} />
        <Route path="/task" element={<Task />} />
        <Route path= "/Calender" element = {<Calender/>}/>
        <Route path= "/Clients" element = {<Clients/>}/>
        <Route path= "/Dashboard" element = {<Dashboard/>}/>
        <Route path= "/Settings" element = {<Settings/>}/>
        <Route path= "/Team" element = {<Team/>}/>
>>>>>>> f251ae727b99e3648c34b19e63e07930c693c0f0
      </Routes>
    </BrowserRouter>
  );
}

<<<<<<< HEAD
export default App;
=======
export default App;
>>>>>>> f251ae727b99e3648c34b19e63e07930c693c0f0
