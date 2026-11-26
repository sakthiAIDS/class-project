import z from "zod";
export const registerschema = z.object({
    name: z.string().min(3,"Name must contain 3 letter"),
    email: z.string().email(3,"Enter a valid email"),
    password: z.string().min(8,"Password should be minimum of 8"),
    age: z.coerce.number().min(18,"Age shpuld be minimum of 18")
})