import React from "react";
import Joi from "joi-browser";
import { NavLink } from "react-router-dom";
import Form from "../../base/form.jsx";

class LoginForm extends Form {
  state = {
    data: {
      username: "",
      password: "",
    },
    errors: {},
    buttonDisabled: false,
  };

  schema = {
    username: Joi.string()
      .required()
      .label("Username"),
    password: Joi.string()
      .required()
      .label("Password")
  };


  render() {
    return (
      <form method="post" onSubmit={this.handleSubmit}>
        <div class="form-group">
          {this.renderInput("username", "Username")}
        </div>
        <div class="form-group">
          {this.renderInput("password", "Password", "password")}
        </div>
        {this.renderButton("Login", this.buttonDisabled)}
        <p class="mt-3 text-center">Don't have an account? <NavLink to="/register">Register</NavLink></p>
      </form>
    );
  }
}

export default LoginForm;
