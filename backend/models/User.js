const Mongoose = require("mongoose")
const Schema = Mongoose.Schema

const UserSchema = new Schema({
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
    profile: {
        photo: {
          type: String,
          default: null,
        },
        additionalInfo: {
          type: Map,
          of: String,
        },
      },
    createdAt: {
    type: Date,
    default: Date.now,
    },
})

const User = Mongoose.model("user", UserSchema)

module.exports = User