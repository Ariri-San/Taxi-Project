import React from "react";
import { useNavigate } from "react-router";
// import { NavLink } from "react-router-dom";
import TravelForm from "./forms/travelForm";


function Travel(props) {
    const navigate = useNavigate();
    const url = "travel/";


    if (props.user) {
        return (
            <div class="row justify-content-center">
                <TravelForm
                        navigate={navigate}
                        urlForm={url}
                        toPath="/"
                    />
            </div>
        );
    }
}

export default Travel;