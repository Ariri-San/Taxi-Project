import React from "react";
import { useNavigate } from "react-router";
import auth from "../services/authService";
// import { NavLink } from "react-router-dom";
import RegisterForm from "./forms/registerForm";


async function doResults(data, results) {
    await auth.login(data.username, data.password);
    window.location = "/";
}


function Register(props) {
    const navigate = useNavigate();
    const url = "auth/users/";

    return (
        <React.Fragment>
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header text-center">
                                <h3>Register</h3>
                            </div>
                            <div class="card-body">
                                <RegisterForm
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

export default Register;
