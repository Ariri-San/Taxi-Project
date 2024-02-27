import React from "react";
import Joi from "joi-browser";
// import { NavLink } from "react-router-dom";
import Form from "../../base/form.jsx";
import request from "../../services/requestService.js";


class TravelForm extends Form {
    state = {
        data: { date: "", date_return: "", passengers: "", luggage: "", origin: "", destination: "" },
        errors: {},
        buttonDisabled: false,
        list: { origin: [], destination: [] }
    };

    schema = {
        origin: Joi.string()
            .required()
            .label("Origin"),
        destination: Joi.string()
            .required()
            .label("Destination"),
        luggage: Joi.string()
            .empty('')
            .label("Number of luggage"),
        passengers: Joi.string()
            .empty('')
            .label("Number of passenger"),
        date: Joi.date()
            .empty('')
            .iso()
            .label("Date"),
        date_return: Joi.date()
            .empty('')
            .iso()
            .label("Date Return"),
    };


    findPlace = async (e) => {
        e.preventDefault();
        var response = null
        if (e.target.value) {
            response = await request.saveObject({ "name": e.target.value }, "find_place/");

            var list_formated_places = this.state.list.destination;
            if (e.target.id === "origin") {
                list_formated_places = this.state.list.origin;
            }
            var check_add = true;
            if (response.data.places !== true) {
                for (const place of response.data.places) {
                    check_add = true

                    for (const old_place of list_formated_places) {
                        if (place.formatted_address === old_place) check_add = false;
                    }
                    if (check_add) {
                        list_formated_places.push(place.formatted_address);
                    }
                }
            }

            if (e.target.id === "origin") {
                this.setState({ ...this.state, list: { ...this.state.list, origin: list_formated_places } });
            }
            else this.setState({ ...this.state, list: { ...this.state.list, destination: list_formated_places } });

        }
    }


    render() {
        return (
            <form onChange={this.findPlace} onSubmit={this.handleSubmit} method="post">
                <div class="form-row">
                    <div class="form-group col-md-6">
                        {this.renderInput("origin", "Origin", "text", "list_origin")}
                        <datalist id="list_origin">
                            {this.state.list.origin.map(place => <option>{place}</option>)}
                        </datalist>
                    </div>
                    <div class="form-group col-md-6">
                        {this.renderInput("destination", "Destination", "text", "list_destination")}
                        <datalist id="list_destination">
                            {this.state.list.destination.map(place => <option>{place}</option>)}
                        </datalist>
                    </div>
                </div>

                <div class="form-group">
                    {this.renderInput("passengers", "Passengers")}
                </div>

                <div class="form-group">
                    {this.renderInput("luggage", "Luggage")}
                </div>

                <div class="form-group">
                    {this.renderInput("date", "Date", "date")}
                </div>

                <div class="form-group">
                    {this.renderInput("date_return", "Return Date", "date")}
                </div>
                {this.renderButton("Generate")}
                {/* <button type="button" class="btn btn-primary" id="generateButton">Generate</button> */}
            </form>
        );
    }
}

export default TravelForm;