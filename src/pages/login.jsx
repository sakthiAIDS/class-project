import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Login() {

<<<<<<< HEAD
    const navigate = useNavigate()

    const [formdata, setFormdata] = useState({
        username: "",
        password: ""
    })

    const [remember, setRemember] = useState(false)

    function handleChange(e) {
        setFormdata({
            ...formdata,
            [e.target.name]: e.target.value
=======
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
>>>>>>> f251ae727b99e3648c34b19e63e07930c693c0f0
        })
    }

    const handlesubmit = (event) => {
        event.preventDefault()
        console.log(formdata)
<<<<<<< HEAD
        alert("Login Successfully")
        navigate('/dashboard', {
            state: formdata
=======
        alert("Login succesfull")
        navigate("/Dashboard",{
          state: formdata
>>>>>>> f251ae727b99e3648c34b19e63e07930c693c0f0
        })
    }

    return (
<<<<<<< HEAD
        <div className="min-h-screen flex justify-center items-center bg-orange-50">

            <div className="bg-white p-8 rounded-lg shadow-md w-80">

                <h1 className="text-2xl font-bold text-center mb-6 text-orange-600">
                    Login
                </h1>

                <form onSubmit={handlesubmit}>

                    <label className="block mb-2">Username</label>

                    <input
                        type="text"
                        placeholder="Enter username"
                        name="username"
                        onChange={handleChange}
                        className="w-full p-2 border border-orange-200 rounded mb-4 outline-none focus:border-orange-500"
                        required
                    />

                    <label className="block mb-2">Password</label>

                    <input
                        type="password"
                        placeholder="Enter password"
                        name="password"
                        onChange={handleChange}
                        className="w-full p-2 border border-orange-200 rounded mb-4 outline-none focus:border-orange-500"
                        required
                    />

                    <div className="flex items-center mb-5">
                        <input
                            type="checkbox"
                            checked={remember}
                            onChange={(e) => setRemember(e.target.checked)}
                            className="accent-orange-500 w-4 h-4"
                        />

                        <label className="ml-2 text-sm text-gray-600">
                            Remember Me
                        </label>
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-orange-500 text-white p-2 rounded hover:bg-orange-600"
                    >
                        Login
                    </button>

                </form>

                <p className="text-center text-sm mt-4">
                    Don't have an account?

                    <span
                        onClick={() => navigate('/register')}
                        className="text-orange-600 cursor-pointer ml-1"
                    >
                        Register
                    </span>
                </p>

            </div>
=======
        <div>
            <h1>Login Page</h1><br></br>

            <form onSubmit={handlesubmit}>
                <input type="text" placeholder="Enter username" name="username" onChange={handleChange}/>
                <br /><br />
                <input type="password" placeholder="Enter password" name="password" onChange={handleChange} />
                <br /><br />
                <button type="submit">Login</button>
            </form>
>>>>>>> f251ae727b99e3648c34b19e63e07930c693c0f0
        </div>
    )
}

export default Login