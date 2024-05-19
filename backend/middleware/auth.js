const jwt = require("jsonwebtoken");
const jwtSecret = process.env.JWT_SECRET;

exports.adminAuth = (req, res, next) => {
  // Extract token from cookie
  const token = req.cookies.jwt;

  // Check if token exists
  if (!token) {
    return res.status(401).json({ message: "Not authorized, token not available" });
  }

  // Verify token
  jwt.verify(token, jwtSecret, (err, decodedToken) => {
    if (err || !decodedToken) {
      return res.status(401).json({ message: "Not authorized" });
    }

    // Check user role
    if (decodedToken.role !== "admin") {
      return res.status(401).json({ message: "Not authorized" });
    }

    // If everything is okay, proceed to the next middleware
    next();
  });
};


exports.userAuth = (req, res, next) => {
    const token = req.cookies.jwt

    if (!token) {
        return res.status(401).json({ message: "Not authorized, token not available" })
    }

    jwt.verify(token, jwtSecret, (err, decodedToken) => {
        if (err || !decodedToken) {
            return res.status(401).json({ message: "Not authorized" })
        }

        if (decodedToken.role !== "Basic") {
            return res.status(401).json({ message: "Not authorized" });
        }

        next()
    })
}
