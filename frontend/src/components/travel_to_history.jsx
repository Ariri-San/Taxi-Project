import React, { useState } from "react";
import { useLocation, useNavigate} from "react-router";
import {StaticGoogleMap, Marker} from 'react-static-google-map';
import request from "../services/requestService";
import getData from '../services/getData';
import ShowData from '../base/showData';
import DeleteData from './../base/deleteData';
import { toast } from "react-toastify";

const token_api = process.env.REACT_APP_GOOGLE_API;



async function doSubmit(id, navigate){
    await request.saveObject({id: id}, "travel_to_history/");
    toast.success(("Travel " + id + " Complited"), {autoClose: 1200});
    await new Promise(resolve => setTimeout(resolve, 2000));
    return window.location.replace("/travel_to_history");
}


function showObject(navigate, location, item) {
    return (
        <main class="main-container" style={{margin: "30px auto"}}>

            <div className="map" style={{borderRadius: "6px"}}>
                <StaticGoogleMap size="650x187" className="img-fluid" apiKey={token_api}>
                    <Marker location={{ lat: item.origin.lat, lng: item.origin.lng }} color="blue" label="A" />
                    <Marker location={{ lat: item.destination.lat, lng: item.destination.lng }} color="red" label="B" />
                    
                </StaticGoogleMap>
            </div>

            <div style={{margin: "10px 5px 5px 5px"}}>
                <DeleteData
                    label="Complete"
                    navigate={navigate}
                    location={location}
                    onSubmit={() => doSubmit(item.id, navigate)}
                    className="btn btn-success primary"
                    title="Complete Travel"
                    body="Are You Sure This Travel Is Ended?"
                ></DeleteData>
                <>  </>
                <DeleteData
                    navigate={navigate}
                    location={location}
                    urlDelete="travel/"
                    toPath="/travel"
                    id={item.id}
                    title="Delete Travel"
                ></DeleteData>
            </div>

            <i></i><p class="price">{item.price} £</p>
            <p class="time">{item.date}</p>
            <p class="hr"></p>
            <i></i><p class="text-1">{item.origin.name}</p>
            <i></i><p class="text-2">{item.destination.name}</p>
        </main>
    );
}


function showObjects(navigate, location, items) {
    return items.map(item => showObject(navigate, location, item));
}


async function setData(setState, state) {
    try {
        if (!state) setState({ data: await getData(null), show: { description: true } });
    } catch (error) {
        request.showError(error);
    }
}


function TravelToHistory(props) {
    const navigate = useNavigate();
    const location = useLocation();


    request.setUrl("travel_to_history/");

    const [state, setState] = useState(0);

    setData(setState, state);

    // console.log(state);


    if (props.user) {
        if (state.data) return (
            <>
                <ShowData
                    url="travel/"
                    data={state.data}
                    showObjects={() => showObjects(navigate, location, state.data)}
                    name="travels"
                ></ShowData>
            </>
        );
    }

}

export default TravelToHistory;
