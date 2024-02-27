import React from "react";
import { useNavigate } from "react-router";
import auth from "../services/authService";
import { NavLink } from "react-router-dom";
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
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header text-center">
                                <h3>Login</h3>
                            </div>
                            <div class="card-body">
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
