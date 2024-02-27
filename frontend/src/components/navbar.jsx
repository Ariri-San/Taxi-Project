import React from "react";
import Package from "../../package.json";
import { NavLink } from "react-router-dom";
// import "../css/navbar.css";
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCartShopping } from '@fortawesome/free-solid-svg-icons'

const api = Package.proxy;


function Navbar({ user }) {
    return (
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a href="home.html">
                {/* <img src="./img/Welwyn Airport Taxis Logo - Black with White Background 2.png" alt="Company Logo" style="width: 67px"> */}
            </a>
            <a class="navbar-brand" href="#">Welwyn Airport Taxis</a>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="login.html" id="loginButton">Login</a>
                        <a class="nav-link" href="home.html">home</a>
                        <a class="nav-link" href="Booked Travels.html">History</a>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;