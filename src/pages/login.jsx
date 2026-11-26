
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const handlesubmit = (event) => {
        event.preventDefault();
        console.log("Login Details:");
        console.log("Email:", email);
        console.log("Password:", password);
        console.log({
            email: email,
            password: password
        });
        navigate('/project');
    };
    return (
        <div>
        <h1>Login Page</h1>
        <form onSubmit={handlesubmit}>
        <input
        type="email"
        placeholder="Enter email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
                />
                <br /><br />
                <input
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <br /><br />
                <button type="submit">Login</button>
            </form>
        </div>
    );
}
export default Login;
