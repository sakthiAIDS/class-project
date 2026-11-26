import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

function Dashboard(){

    const location = useLocation();
    const[userdata,setuserdata] = useState("");

    function displaydata(){
        setuserdata(location.state);
        console.log(userdata)
    }

    return(
        <div>
        <h1>Dashboard</h1>
        <button onClick ={displaydata}>Button</button>
        </div>
    );
}
export default Dashboard