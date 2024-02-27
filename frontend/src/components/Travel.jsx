import React from "react";
import { useNavigate } from "react-router";
import { NavLink } from "react-router-dom";
import TravelForm from "./forms/travelForm";



function Travel(props) {
    const navigate = useNavigate();
    const url = "travel/";


    if (props.user) {
        return (
            <div class="row justify-content-center">
                <div class="col-md-6 text-center">
                    <h2>Welcome to our Taxi Booking Service</h2>
                    <p>Book your taxi conveniently with our online platform.</p>

                    <div class="alert alert-info" role="alert">
                        Enjoy a comfortable and hassle-free taxi experience with our reliable service!
                    </div>
                    <TravelForm
                        navigate={navigate}
                        urlForm={url}
                        toPath="/"
                    />
                </div>
            </div>
        );
    }
    else {
        return navigate("/")
    }

}

export default Travel;