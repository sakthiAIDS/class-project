import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

function Login() {

    //const [email, setEmail] = useState("")
    //const [password, setPassword] = useState("")

    const navigate = useNavigate();
    const location = useLocation();
    const[logindata,setFormdata] = useState({
        username:"",
        password:""
    })

    function handleChange(e){
        e.preventDefault();
        setFormdata({
            ...logindata,
            [e.target.name]:e.target.value
        })
    }

    const handlesubmit = (event) => {
        event.preventDefault()
        const registerdata = location.state
        console.log("login data",logindata)
        console.log("register data",registerdata)
        if(logindata.username == registerdata.name && logindata.password == registerdata.password){
            navigate("./dashboard",{
                state:logindata
            })
        }else{
            console.log("Invalid Credentials")

        }
    }

    return (
        <div className="min-h-screen bg-green-100 flex justify-center items-center">
            <form onSubmit={handlesubmit} className="bg-white w-96 p-8 rounded-lg shadow-lg">
            
            <h1 className="text-2xl font-bold text-center mb-6">Login Page</h1>

            
            <label className="block font-medium mb-2">Username</label>
            <input className="w-full border p-2 rounded mb-4 outline-none focus:border-blue-500" type="text" placeholder="Enter username" name="username" onChange={handleChange} />

            <label className="block font-medium mb-2">Password</label>
            <input className="w-full border p-2 rounded mb-5 outline-none focus:border-blue-500" type="password" placeholder="Enter password" name="password" onChange={handleChange} />

            <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Login</button>

        </form>

        </div>
    )
}

export default Login