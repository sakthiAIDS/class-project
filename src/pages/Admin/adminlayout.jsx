import { Link, Outlet } from "react-router-dom";

function Adminlayout() {
    return ( 
        <div>
       <nav>
        
        <Link to={"Admindashboard"}>Admindashboard</Link>
        <Link to={"Settings"}>Settings</Link>
        <Link to={"userdetails"}>userdetails</Link>
       </nav>
        <Outlet/>
       </div>
       
     );
}

export default Adminlayout;