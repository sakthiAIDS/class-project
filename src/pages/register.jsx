import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate } from 'react-router-dom'
import { registerschema } from './schema'

function Register() {
    const navigate = useNavigate();
    const {register,handleSubmit,formstate:{errors}} = useForm({
        resolver:zodResolver(registerschema)
    })

    function onsubmit1(data){
        console.log(data)
        alert("register sucess")
        navigate("/")
    }
    return ( 
    <>
      <form onSubmit={handleSubmit(onsubmit1)}>
        <input type="text" placeholder="Enter name" {...register("name")}/> <br /><br />
        <p>{errors.name?.message}</p>
        <input type="email" placeholder="Enter Email" {...register("email")}/> <br /><br />
        <p>{errors.name?.message}</p>
        <input type="text" placeholder="Enter password" {...register("password")}/> <br /><br />
        <p>{errors.name?.message}</p>
        <input type="text" placeholder="Enter age" {...register("age")}/> <br /><br />
        <p>{errors.name?.message}</p>
        
        
        <button type="submit">Submit</button>
        </form>
    </>
     );
}

export default Register;