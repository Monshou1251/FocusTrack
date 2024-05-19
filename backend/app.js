const express = require("express");
const dotenv = require("dotenv");
const connectDB = require("./config/db");
const cookieParser = require("cookie-parser")
const { adminAuth, userAuth } = require("./middleware/auth")


dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());
app.use(cookieParser());
app.use("/api/auth", require("./routes/authRoutes"));

app.get("/admin", adminAuth, (req, res) => res.send("Admin Route"))
app.get("/basic", userAuth, (req, res) => res.send("User Route"))

connectDB();

const server = app.listen(PORT, () =>
  console.log(`Server connected to port ${PORT}`)
);

process.on("unhandledRejection", (err) => {
  console.log(`An error occurred: ${err.message}`);
  server.close(() => process.exit(1));
});
