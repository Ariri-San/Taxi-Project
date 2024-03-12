import React from "react";
import { useNavigate } from "react-router";
import auth from "../services/authService";
// import { NavLink } from "react-router-dom";
import LoginForm from "./forms/loginForm";



function doResults(data, results) {
    auth.loginWithJwt(results.data.access, results.data.refresh);
    window.location = "/";
}



function Login(props) {
    const navigate = useNavigate();
    const url = "auth/jwt/create/";

    return (
        <React.Fragment>
            <div className="container mt-5">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-header text-center">
                                <h3>Login</h3>
                            </div>
                            <div className="card-body">
                                <LoginForm
                                    navigate={navigate}
                                    onResults={doResults}
                                    urlForm={url}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>  
        </React.Fragment>
    );
}

export default Login;
