import { BrowserRouter, Routes, Route } from "react-router-dom";
import Aboutus from "./pages/aboutus";
import Task from "./pages/task";
import Login from "./pages/login";
import Team from "./pages/team";
import Clients from "./pages/clients";
import Dashboard from "./pages/dashboard";
import Calender from "./pages/calender";
import Settings from "./pages/settings";
import Register from "./pages/register";


function App(){
  return(
    <BrowserRouter>
    <Routes>
      <Route path ="/Login" element={<Login/>}/>
      <Route path ="/Aboutus" element={<Aboutus/>}/>
      <Route path ="/Task" element={<Task/>}/>
      <Route path ="/Team" element={<Team/>}/>
      <Route path ="/Clients" element={<Clients/>}/>
      <Route path ="/Dashboard" element={<Dashboard/>}/>
      <Route path ="/Calender" element={<Calender/>}/>
      <Route path ="/Settings" element={<Settings/>}/>
      <Route path ="/Register" element={<Register/>}/>
    </Routes>
    </BrowserRouter>

    
  )
}

export default App;