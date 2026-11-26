import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Login() {

    //const [email, setEmail] = useState("")
    //const [password, setPassword] = useState("")

    const navigate = useNavigate()

    const[formdata,setFormdata] = useState({
        username:"",
        password:""
    })

    function handleChange(e){
        e.preventDefault();
        setFormdata({
            ...formdata,
            [e.target.name]:e.target.value
        })
    }

    const handlesubmit = (event) => {
        event.preventDefault()
        console.log(formdata)
        alert("Login succesfull")
        navigate("/Dashboard",{
          state: formdata
        })
    }

    return (
        <div>
            <h1>Login Page</h1><br></br>

            <form onSubmit={handlesubmit}>
                <input type="text" placeholder="Enter username" name="username" onChange={handleChange}/>
                <br /><br />
                <input type="password" placeholder="Enter password" name="password" onChange={handleChange} />
                <br /><br />
                <button type="submit">Login</button>
            </form>
        </div>
    )
}

export default Login