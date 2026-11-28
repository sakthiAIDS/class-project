import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

function Dashboard(){

    const location = useLocation();
    const[userdata,setUserdata] = useState("");

    //function displaydata(){
    //    setUserdata(location.state);
    //   console.log(userdata)
    //}

    useEffect(()=>{
        setUserdata(location.state);
        console.log(userdata)
    },[]);
    return(
        <div>
        <h1>Dashboard</h1>
        <button> {userdata?.username}</button><br></br>
        <button>{userdata?.password}</button>
        
        </div>
    );
}
export default Dashboard