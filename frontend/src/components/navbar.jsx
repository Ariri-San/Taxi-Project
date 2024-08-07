import React, { useState } from "react";
import { useLocation } from "react-router";
import { NavLink } from "react-router-dom";
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

// const api = Package.proxy;

function check_path(state, path){
    return state.path === path ? "active" : "";
}


function Navbar({ user }) {
  const location = useLocation();
  const [state, setState] = useState({path:location.pathname.slice(1)});

  return ( 
      <nav className="navbar navbar-inverse">
      <div className="container-fluid">
        <div className="navbar-header">
          <NavLink className="navbar-brand" onClick={() => setState({path:"home"})} to="/">Airport Taxis</NavLink>
        </div>
        <ul className="nav navbar-nav">
          <li className={check_path(state, "home")}><NavLink onClick={() => setState({path:"home"})} to="/">Home</NavLink></li>
          <li className={check_path(state, "travel")}>{user ? <NavLink onClick={() => setState({path:"travel"})} to="/travel">Book Taxi</NavLink>: ""}</li>
          <li className={check_path(state, "travels")}>{user ? <NavLink onClick={() => setState({path:"travels"})} to="/travels">Travels</NavLink>: ""}</li>
          <li className={check_path(state, "history")}>{user ? <NavLink onClick={() => setState({path:"history"})} to="/history">History</NavLink>: ""}</li>
          {user && <li className={check_path(state, "travel_to_history")}>{user.is_admin ? <NavLink onClick={() => setState({path:"travel_to_history"})} to="/travel_to_history">Travel to History</NavLink>: ""}</li>}
        </ul>
        <ul className="nav navbar-nav navbar-right">
          <li className={check_path(state, "register")}>{user ? <p style={{color:"white", margin:"20px"}}>{user.username}</p> : <NavLink onClick={() => setState({path:"register"})} className="glyphicon glyphicon-user" to="/register"> Sign Up</NavLink>}</li>
          <li className={check_path(state, "login")}>{user ? <NavLink className="glyphicon glyphicon-log-out" to="/logout"> Logout</NavLink> : <NavLink onClick={() => setState({path:"login"})} className="glyphicon glyphicon-log-in" to="/login"> Login</NavLink>}</li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;