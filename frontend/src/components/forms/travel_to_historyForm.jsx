import React from "react";
import Joi from "joi-browser";
// import { NavLink } from "react-router-dom";
import Form from "../../base/form.jsx";
import request from "../../services/requestService.js";


class TravelToHistoryForm extends Form {
    state = {
        data: { id: "" },
        errors: {},
        buttonDisabled: false,
        list: { origin: [], destination: [] }
    };

    schema = {
        id: Joi.string()
            .empty('')
            .label("ID"),
    };



    render() {
        return (
            <form onChange={this.findPlace} onSubmit={this.handleSubmit} method="post">
                <div class="form-group">
                    {this.renderInput("id", "ID Travel")}
                </div>
                {this.renderButton("Complite")}
            </form>
        );
    }
}

export default TravelToHistoryForm;