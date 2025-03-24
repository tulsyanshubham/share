import mongoose from 'mongoose';
import dotenv from "dotenv";

dotenv.config();

const mongoURL = process.env.MONGO_URI;

const connectDB = async () => {
    await mongoose.connect(mongoURL).then(() => console.log("Connected to MongoDB Successfully"))
}

export default connectDB;