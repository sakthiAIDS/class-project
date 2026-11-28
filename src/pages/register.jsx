import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { registerschema } from "../components/FormSchema/registerschema";
import { zodResolver } from "@hookform/resolvers/zod";

function Register() {
    const navigate=useNavigate();
    const {register, handleSubmit, formState:{errors}}=useForm({
        resolver: zodResolver(registerschema)
    })
    function onSubmit1(data){
        console.log(data)
        alert("register succes")
        navigate("/",{
            state:data
        })
    }
    return (
        <>
        <div className="min-h-screen  bg-green-100 flex justify-center items-center">
        <form onSubmit={handleSubmit(onSubmit1)} className="bg-white p-8 rounded-lg shadow-lg w-96">
            
             <h1 className="text-2xl font-bold text-center mb-6">Register</h1>
            
            <label className="block mb-2 font-medium">Name</label>
            <div className="flex items-center gap-2 mb-4">
            <input className="w-full border p-2 rounded" placeholder="Enter your name" type="text" {...register("name")} />
            <p>{errors.name?.message}</p>
            </div>


            <label className="block mb-2 font-medium">Email</label>
            <div className="flex items-center gap-2 mb-4">
            <input className="w-full border p-2 rounded" placeholder="Enter your name" type="email" {...register("email")} />
            <p>{errors.email?.message}</p>
            </div>

            <label className="block mb-2 font-medium">Password</label>
            <div className="flex items-center gap-2 mb-4">
            <input className="w-full border p-2 rounded"  placeholder="Enter Password"  type="password" {...register("password")} />
            <p>{errors.password?.message}</p>
            </div>

            <label className="block mb-2 font-medium">Age</label>
            <div className="flex items-center gap-2 mb-4">
            <input className="w-full border p-2 rounded" placeholder="Enter your age"  type="number" {...register("age")} />
            <p>{errors.age?.message}</p>
            </div>

            <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Submit</button>
        </form>
        </div>
        </>
    );
}

export default Register;