import React from "react";
import Joi from "joi-browser";
// import { NavLink } from "react-router-dom";
import Form from "../../base/form.jsx";
import request from "../../services/requestService.js";
import {StaticGoogleMap, Marker} from 'react-static-google-map';
import config from "../../config.json";

const token_api = config.TokenApiMap;


class TravelForm extends Form {
    state = {
        data: { date: "", date_return: "", passengers: "", luggage: "", origin: "", destination: "" },
        errors: {},
        buttonDisabled: false,
        list_origin: [],
        list_destination: [],
        location_origin: {},
        location_destination: {},
        check_show:{ date: false, date_return: false, price: false},
        distance_data: {}
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

            var list_places = this.state.list_destination;
            if (e.target.id === "origin") {
                list_places = this.state.list_origin;
            }
            var check_add = true;
            if (response.data.places !== true) {
                for (const place of response.data.places) {

                    if (e.target.value === place.formatted_address){
                        if (e.target.id === "origin") {
                            this.setState({ location_origin: place.geometry.location });
                        }
                        else this.setState({ location_destination: place.geometry.location });
                    }
                    
                    check_add = true
                    for (const old_place of list_places) {
                        if (place.formatted_address === old_place.formatted_address) check_add = false;
                            
                    }
                    if (check_add) {
                        list_places.push(place);
                    }
                }
            }

            if (e.target.id === "origin") {
                this.setState({ list_origin: list_places });
            }
            else this.setState({ list_destination: list_places });

        }
    }

    show_price= async() => {
        if (this.state.data.origin && this.state.data.destination){
            this.setState({check_show: {...this.state.check_show, price: true}});
            var response = await request.saveObject({ "origin": this.state.data.origin , "destination": this.state.data.destination }, "find_distance/");
            this.setState({distance_data: response.data, buttonDisabled: true});
        }
    }

    chenge_check_box = (e) => {
        if (e.target.id=== "returnTravel") this.setState({check_show: {...this.state.check_show, date_return: !this.state.check_show.date_return}});
        else if (e.target.id=== "pickUpASAP") this.setState({check_show: {...this.state.check_show, date: false}});
        else if (e.target.id=== "pickUpLater") this.setState({check_show: {...this.state.check_show, date: true}});
    }


    render() {
        return (
            <>
                <div class="col-md-6 text-center">
                    <h2>Welcome to our Taxi Booking Service</h2>
                    <p>Book your taxi conveniently with our online platform.</p>

                    <div class="alert alert-info" role="alert">
                        Enjoy a comfortable and hassle-free taxi experience with our reliable service!
                    </div>
                    <form onChange={this.findPlace} onSubmit={this.handleSubmit} method="post">
                        <div class="form-row">
                            <div class="form-group col-md-6">
                                {this.renderInput("origin", "Origin", "text", "list_origin")}
                                <datalist id="list_origin">
                                    {this.state.list_origin[0] ? this.state.list_origin.map(place => <option>{place.formatted_address}</option>) : ""}
                                </datalist>
                            </div>
                            <div class="form-group col-md-6">
                                {this.renderInput("destination", "Destination", "text", "list_destination")}
                                <datalist id="list_destination">
                                    {this.state.list_destination[0] ? this.state.list_destination.map(place => <option>{place.formatted_address}</option>) : ""}
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
                            <label for="pickUpOption">Pick-up Option:</label>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="pickUpOption" id="pickUpASAP" value="ASAP" checked={!this.state.check_show.date} onClick={this.chenge_check_box}/>
                                <label class="form-check-label" for="pickUpASAP">
                                    Pick-up ASAP
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="pickUpOption" id="pickUpLater" value="Later"  checked={this.state.check_show.date} onClick={this.chenge_check_box}/>
                                <label class="form-check-label" for="pickUpLater">
                                    Pick-up Later
                                </label>
                                <div class="form-group" id="pickUpLaterDateField" style={{display: this.state.check_show.date ? "block" : "none"}}>
                                    <label for="pickUpLaterDate">Pick-up Date:</label>
                                    {this.renderInput("date", "Date", "datetime-local")}
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="returnTravel" name="returnTravel" onClick={this.chenge_check_box} checked={this.state.check_show.date_return}/>
                                <label class="form-check-label" for="returnTravel">
                                    Return Travel Required
                                </label>
                                <div class="form-group" id="returnDateField" style={{display: this.state.check_show.date_return ? "block" : "none"}}>
                                    {this.renderInput("date_return", "Return Date", "datetime-local")}
                                </div>
                            </div>
                        </div>

                        <button disabled={this.validate()} type="button" class="btn btn-primary" id="generateButton" onClick={this.show_price}>Gnarate</button>

                        <div id="priceDisplay" style={{display: this.state.check_show.price ? "block" : "none"}}>
                            <h4>Estimated Price:</h4>
                            <p id="priceAmount">Price Per Mile: {this.state.distance_data.price_per_mile} £ - Price: {this.state.distance_data.price} £</p>
                            <p id="duration">Mile: {this.state.distance_data.mile} - Duration: {this.state.distance_data.duration}</p>
                        </div>

                        {this.renderButton("Book Taxi", false, "btn btn-primary", {display: this.state.buttonDisabled ? "" : "none"})}
                    </form>
                </div>

                {(this.state.location_destination.lat || this.state.location_origin.lat) ? 
                    <div>
                        <StaticGoogleMap size="400x600" className="img-fluid" apiKey={token_api}>
                            <Marker location={{ lat: this.state.location_origin.lat, lng: this.state.location_origin.lng }} color="blue" label="A" />
                            <Marker location={{ lat: this.state.location_destination.lat, lng: this.state.location_destination.lng }} color="red" label="B" />
                        </StaticGoogleMap>
                    </div> : ""}
                
            </>
        );
    }
}

export default TravelForm;