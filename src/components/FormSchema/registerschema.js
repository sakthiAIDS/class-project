import z from "zod";
export const registerschema = z.object({
    name:z.string().min(3,"Name must contains 3 letter"),
    email:z.string().email("enter a valid Email"),
    password:z.string().min(8,"Password must have 8 "),
    age:z.coerce.number().min(18,"Age min of 18"),
})