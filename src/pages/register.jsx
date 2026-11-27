
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { registerschema } from "../components/FormSchema/registerschema";
import { zodResolver } from "@hookform/resolvers/zod";

function Register() {

    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm({
        resolver: zodResolver(registerschema)
    });

    function onSubmit1(data) {
        console.log(data);
        alert("Register Success");
        navigate("/");
    }

    return (
        <div className="min-h-screen flex justify-center items-center bg-orange-50">

            <form
                onSubmit={handleSubmit(onSubmit1)}
                className="bg-white p-8 rounded-lg shadow-md w-80"
            >

                <h1 className="text-2xl font-bold text-center mb-6 text-orange-600">
                    Register
                </h1>

                <label className="block mb-2">Name</label>

                <input
                    placeholder="Enter your name"
                    type="text"
                    {...register("name")}
                    className="w-full p-2 border border-orange-200 rounded mb-1 outline-none focus:border-orange-500"
                />

                <p className="text-red-500 text-xs mb-3">
                    {errors.name?.message}
                </p>

                <label className="block mb-2">Email</label>

                <input
                    placeholder="Enter your email"
                    type="email"
                    {...register("email")}
                    className="w-full p-2 border border-orange-200 rounded mb-1 outline-none focus:border-orange-500"
                />

                <p className="text-red-500 text-xs mb-3">
                    {errors.email?.message}
                </p>

                <label className="block mb-2">Password</label>

                <input
                    placeholder="Enter password"
                    type="password"
                    {...register("password")}
                    className="w-full p-2 border border-orange-200 rounded mb-1 outline-none focus:border-orange-500"
                />

                <p className="text-red-500 text-xs mb-3">
                    {errors.password?.message}
                </p>

                <label className="block mb-2">Age</label>

                <input
                    placeholder="Enter your age"
                    type="number"
                    {...register("age")}
                    className="w-full p-2 border border-orange-200 rounded mb-1 outline-none focus:border-orange-500"
                />

                <p className="text-red-500 text-xs mb-3">
                    {errors.age?.message}
                </p>

                <button
                    type="submit"
                    className="w-full bg-orange-500 text-white p-2 rounded hover:bg-orange-600"
                >
                    Register
                </button>

                <p className="text-center text-sm mt-4">
                    Already have an account?

                    <span
                        onClick={() => navigate("/")}
                        className="text-orange-600 cursor-pointer ml-1"
                    >
                        Login
                    </span>
                </p>

            </form>
        </div>
    );
}

export default Register;
