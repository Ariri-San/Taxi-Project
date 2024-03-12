import React, { useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router";
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


function History(props) {
    const params = useParams();
    const navigate = useNavigate();
    const location = useLocation();

    request.setUrl("history/");

    const [state, setState] = useState(0);

    setData(params.id, setState, state);

    // console.log(state);


    if (props.user) {
        if (state.data) return (
            <ShowData data={state.data} showObjects={showObjects} name="arts"></ShowData>
        )
    }
    else {
        return navigate("/")
    }

}

export default History;