import React from "react";


async function setData(id, setState, state) {
    try {
        if (!state) setState({ data: await getData(null, id), show: { description: true } });
    } catch (error) {
        request.showError(error);
    }
}


function History() {
    const defaultProps = {
        center: {
            lat: 56.1164654,
            lng: -3.925842000000001
        },
        zoom: 15
    };

    return (
        // Important! Always set the container height explicitly
        <div style={{ height: '30vh', width: '30%' }}>
            <GoogleMapReact
                bootstrapURLKeys={{ key: "AIzaSyDEnymewL5xuqEqp3baWmzXley4_iUdYdk" }}
                defaultCenter={defaultProps.center}
                defaultZoom={defaultProps.zoom}
            >
                <AnyReactComponent
                    lat={56.1164654}
                    lng={-3.925842000000001}
                    text="My Marker"
                />
            </GoogleMapReact>
        </div>
    );
}


export default History;