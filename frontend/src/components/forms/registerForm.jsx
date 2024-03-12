import React from "react";
import Joi from "joi-browser";
import { NavLink } from "react-router-dom";
import Form from "../../base/form.jsx";

class RegisterForm extends Form {
  state = {
    data: { username: "", password: "", email: "", phone: "" },
    errors: {},
    buttonDisabled: false,
  };

  schema = {
    username: Joi.string()
      .required()
      .label("Username"),
    password: Joi.string()
      .required()
      .min(8)
      .label("Password"),
    email: Joi.string()
      .email()
      .required()
      .label("Email"),
    phone: Joi.string()
      .required()
      .min(10)
      .max(15)
      .label("Phone")
  };


  render() {
    return (
      <form onSubmit={this.handleSubmit} method="post">
        <div class="form-group">
          {this.renderInput("email", "Email")}
        </div>
        <div class="form-group">
          {this.renderInput("phone", "Phone")}
        </div>
        <div class="form-group">
          {this.renderInput("username", "Username")}
        </div>
        <div class="form-group">
          {this.renderInput("password", "Password", "password")}
        </div>
        {this.renderButton("Register", this.buttonDisabled, "btn btn-success btn-block")}
        <p class="mt-3 text-center">Already have an account? <NavLink to="/login">Login</NavLink></p>
      </form>
    );
  }
}

export default RegisterForm;
