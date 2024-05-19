const User = require("../models/User");
const bcrypt = require('bcrypt');
require('dotenv').config()

const jwt = require('jsonwebtoken');

exports.register = async (req, res, next) => {
  const { username, password, email } = req.body;

  if (!username || !password || !email) {
    return res.status(400).json({ message: "Username, Password, and Email are required" });
  }

  if (password.length < 6) {
    return res.status(400).json({ message: "Password must be at least 6 characters long" });
  }

  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await User.create({
      username,
      password: hashedPassword,
      email,
    });

    const maxAge = 3 * 60 * 60; // 3 hours in seconds
    const token = jwt.sign(
      { id: user._id, username: user.username, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: maxAge }
    );

    res.cookie('jwt', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production', 
      maxAge: maxAge * 1000, // Convert to milliseconds
    });

    res.status(201).json({
      message: "User successfully created",
      user: user._id,
    });
  } catch (error) {
    res.status(400).json({
      message: "User not successfully created",
      error: error.message,
    });
  }
};


exports.login = async (req, res, next) => {
  const { username, password } = req.body;

  // Validate input
  if (!username || !password) {
    return res.status(400).json({
      message: "Username or Password not provided",
    });
  }

  try {
    // Find user by username
    const user = await User.findOne({ username });

    if (!user) {
      return res.status(401).json({
        message: "Login not successful",
        error: "User not found",
      });
    }

    // Compare passwords
    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
      return res.status(401).json({
        message: "Login not successful",
        error: "Incorrect password",
      });
    }

    // Generate JWT token
    const token = jwt.sign({ id: user._id, username: user.username, role: user.role }, process.env.JWT_SECRET, { expiresIn: '1h' });
    // Set JWT token as a cookie
    const maxAge = 60 * 60; // 1 hour in seconds
    res.cookie('jwt', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production', 
      maxAge: maxAge * 1000, // Convert to milliseconds
    });

    // Send success response
    res.status(200).json({
      message: "Login successful",
      user: { id: user._id, username: user.username },
      token,
    }); 

  } catch (error) {
    // Handle errors
    res.status(500).json({
      message: "An error occurred",
      error: error.message,
    });
  }
};



exports.update = async (req, res, next) => {
  const { role, id } = req.body;

  // Verifying if role and id are present
  if (!role || !id) {
    return res.status(400).json({ message: "Role or Id not present" });
  }

  // Verifying if the value of role is admin
  if (role !== "admin") {
    return res.status(400).json({ message: "Role is not admin" });
  }

  try {
    const user = await User.findById(id);

    // Verifies the user exists and is not already an admin
    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }

    if (user.role === "admin") {
      return res.status(400).json({ message: "User is already an Admin" });
    }

    user.role = role;
    await user.save();

    res.status(200).json({ message: "Update successful", user });
  } catch (error) {
    res.status(500).json({ message: "An error occurred", error: error.message });
  }
};


exports.deleteUser = async (req, res, next) => {
  const { id } = req.body;

  // Check if ID is provided
  if (!id) {
    return res.status(400).json({ message: "User ID not provided" });
  }

  try {
    const user = await User.findByIdAndDelete(id);

    // Check if user was found and deleted
    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }

    res.status(200).json({ message: "User successfully deleted", user });
  } catch (error) {
    res.status(500).json({ message: "An error occurred", error: error.message });
  }
};
