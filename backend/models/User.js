const Mongoose = require("mongoose")

const UserSchema = new Mongoose.Schema({
    username: {
        type: String,
        unique: true, 
        required: true,
    },
    password: {
        type: String,
        minlength: 6, 
        required: true,
    },
    email: {
        type: String,
        minlength: 6, 
        required: true,
        match: [/.+\@.+\..+/, "Please enter a valid email address"]
    },
    role: {
       type: String,
       default: "Basic",
       required: true, 
    },
})

const User = Mongoose.model("user", UserSchema)

module.exports = User