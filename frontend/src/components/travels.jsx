import React, { useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router";
import {StaticGoogleMap, Marker} from 'react-static-google-map';
import request from "../services/requestService";
import getData from '../services/getData';
import ShowData from '../base/showData';
// import config from "../config.json";

const token_api = process.env.REACT_APP_GOOGLE_API;



function showObject(item) {
    return (
        <main className="main-container" style={{margin: "30px auto"}}>
            <div className="map" style={{borderRadius: "6px"}}>
                <StaticGoogleMap size="650x190" className="img-fluid" apiKey={token_api}>
                    <Marker location={{ lat: item.origin.lat, lng: item.origin.lng }} color="blue" label="A" />
                    <Marker location={{ lat: item.destination.lat, lng: item.destination.lng }} color="red" label="B" />
                    
                </StaticGoogleMap>
            </div>
            <p className="comment">ID: {item.id}</p>
            <i></i><p className="price">{item.price} £</p>
            <p className="time">{item.date}</p>
            <p className="hr"></p>
            <i></i><p className="text-1">{item.origin.name}</p>
            <i></i><p className="text-2">{item.destination.name}</p>
        </main>
    );
}


function showObjects(items) {
    return items.map(item => showObject(item));
}



async function setData(setState, state) {
    try {
        setState({ ...state, data: await getData(), change: true });
    } catch (error) {
        request.showError(error);
        setState({ ...state, change: true });
    }
}


function Travels(props) {
    request.setUrl("travel/");

    const [state, setState] = useState(0);

    if (!state.change) setData(setState, state);
    else {
        if (props.user) {
            if (state.data) return (
                <ShowData data={state.data} showObjects={showObjects} name="travels"></ShowData>
            );
        }
    }

}

export default Travels;