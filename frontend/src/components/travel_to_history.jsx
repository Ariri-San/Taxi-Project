import React, { useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router";
import TravelToHistoryForm from "./forms/travel_to_historyForm";
import request from "../services/requestService";
import getData from '../services/getData';
import ShowData from '../base/showData';



function showObject(item) {
    return (
        <main class="main-container" style={{margin: "30px auto"}}>

            <div class="map"></div>
            <p class="comment">ID: {item.id}</p>
            <i></i><p class="price">{item.price} £</p>
            <p class="time">{item.date}</p>
            <p class="hr"></p>
            <i></i><p class="text-1">{item.origin}</p>
            <i></i><p class="text-2">{item.destination}</p>
        </main>
    );
}


function showObjects(items) {
    return items.map(item => showObject(item));
}


async function setData(id, setState, state) {
    try {
        if (!state) setState({ data: await getData(null, id), show: { description: true } });
    } catch (error) {
        request.showError(error);
    }
}


function TravelToHistory(props) {
    const params = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    // const url = "travel/";


    request.setUrl("travel_to_history/");

    const [state, setState] = useState(0);

    setData(params.id, setState, state);

    // console.log(state);


    if (props.user) {
        if (state.data) return (
            <>
                <ShowData url="travel/" data={state.data} showObjects={showObjects} name="arts"></ShowData>
                <div className="row justify-content-center" style={{margin: "50px"}}>
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-header text-center">
                                <h3>Complite Travel</h3>
                            </div>
                            <div className="card-body">
                                <TravelToHistoryForm
                                    navigate={navigate}
                                    toPath="/travel_to_history"
                                /> 
                            </div>
                        </div>
                    </div>
                </div>
            </>
        );
    }

}

export default TravelToHistory;
