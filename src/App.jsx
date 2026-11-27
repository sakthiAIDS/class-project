import { BrowserRouter, Routes, Route } from "react-router-dom";

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

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Login />} />
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

      </Routes>
    </BrowserRouter>
  );
}

export default App;