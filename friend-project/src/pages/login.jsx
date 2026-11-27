import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

function Login(){
    const Navigate=useNavigate();
    const[formdata,setformdata]=useState({
    username:" ",
    password:" "
  })

  function handle(e){
    setformdata({
      ...formdata,
      [e.target.name]:e.target.value
    });
  }

  function print(e){
    e.preventDefault();
    console.log(formdata)
    alert("print successful")
    Navigate("/dashboard")
  }

    return(
      <form onSubmit={print}> 
      <label>UserName:</label>
      <input type="text" placeholder="Enter the name: " required value={formdata.username} name="username" onChange={handle}/><br></br>
      <label>Password:</label>
      <input type="password" placeholder="Enter the pass: " required value={formdata.password} name="password" onChange={handle}/><br></br>
      <button type="submit">SUBMIT</button>
    </form>
    );
}
export default Login;