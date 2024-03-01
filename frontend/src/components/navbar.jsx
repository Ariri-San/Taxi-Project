import React from "react";
import Package from "../../package.json";
import { NavLink } from "react-router-dom";
// import "../css/navbar.css";
import "../templates/css/styale.css";
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
                        {user ? <p>{user.username}</p> : <NavLink class="nav-link" to="/login">Login</NavLink>}
                        <NavLink class="nav-link" to="/home">home</NavLink>
                        <NavLink class="nav-link" to="/travels/add">Book Taxi</NavLink>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;