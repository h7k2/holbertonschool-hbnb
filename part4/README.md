# HBnB - Part 4: Simple Web Client

This project is the front-end part of the HBnB application (Holberton School).  
After building the API in previous parts, this section focuses on creating a simple web client using **HTML5**, **CSS3**, and **JavaScript ES6**, fully connected to the back-end via **Fetch API** and **JWT authentication**.

🔧 How to Run the Project

To start the application, you must run Part 3 (Back-End API) first, then Part 4 (Front-End client).

1️⃣ Start the Part 3 API

Go to the Part 3 directory:

cd part3/hbnb


Run the API server:

python3 run.py


Keep this terminal open.

2️⃣ Start the Part 4 Front-End

Open a new terminal window, then go to the Part 4 directory:

cd part4


Run the command to start the front-end server:

python3 -m http.server 8080


Your back-end and front-end should now be running together.

## 🚀 Features

### 🔐 Login
- Login form connected to the API (`/api/auth/login`)
- Stores the JWT token in cookies
- Redirects the user to the main page after authentication

### 🏠 Index Page (List of Places)
- Fetches places from the API
- Displays them as place cards (name, price, details button)
- Client-side filtering by price
- Shows or hides the login button depending on authentication status

### 📄 Place Details
- Displays detailed information about a selected place  
  (name, description, host, price, amenities, reviews)
- “Add Review” button visible only when logged in

### ✍️ Add Review
- Review form available only for authenticated users
- Submits the review to the API
- Redirects unauthenticated users back to the index page

## 🧰 Technologies Used
- **HTML5**  
- **CSS3**  
- **JavaScript (ES6)**  
- **Fetch API**  
- **JWT Authentication**  
- **Flask API (backend)**

## 🎯 Goal of This Part
Build a simple interface that communicates with the HBnB API, allowing users to:
- authenticate,
- browse places,
- see details,
- and add reviews.

This concludes the front-end portion of the HBnB v2 project.
