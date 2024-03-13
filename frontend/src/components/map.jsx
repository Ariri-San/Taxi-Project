import React from "react";
import GoogleMapReact from 'google-map-react';
import {StaticGoogleMap, Marker, Path} from 'react-static-google-map';
import config from "../config.json";

const token_api = config.TokenApiMap;

const AnyReactComponent = ({ text }) => <div>{text}</div>;

function SimpleMap() {
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
            {/* <GoogleMapReact
                bootstrapURLKeys={{ key: token_api }}
                defaultCenter={defaultProps.center}
                defaultZoom={defaultProps.zoom}
            >
                <AnyReactComponent
                    lat={56.1164654}
                    lng={-3.925842000000001}
                    text="My Marker"
                />
            </GoogleMapReact> */}


            <StaticGoogleMap size="600x600" className="img-fluid" apiKey={token_api}>
                <Marker location="6.4488387,3.5496361" color="blue" label="P" />
                <Marker location={{ lat: 40.737102, lng: -73.990318 }} color="blue" label="T" />
                
            </StaticGoogleMap>

            <p></p>

            <StaticGoogleMap size="600x600" apiKey={token_api}>
                <Marker.Group>
                    <Marker location="40.737102,-73.990318" label="T" />
                    <Marker location="40.749825,-73.987963" />
                </Marker.Group>
            </StaticGoogleMap>

            <p></p>

            <StaticGoogleMap size="6000x6000" apiKey={token_api}>
                <Marker
                    location={{ lat: 40.737102, lng: -73.990318 }}
                    color="blue"
                    label="P"
                />
                <Path
                    points={[
                    '40.737102,-73.990318',
                    '40.749825,-73.987963',
                    '40.752946,-73.987384',
                    '40.755823,-73.986397',
                    ]}
                />
            </StaticGoogleMap>

            <StaticGoogleMap size="600x600" apiKey={token_api}>
            <Marker iconURL="https://goo.gl/1oTJ9Y" location="Canberra+ACT" />
            <Marker
                anchor="topleft"
                iconURL="http://tinyurl.com/jrhlvu6"
                location="Melbourne+VIC"
            />
            <Marker
                anchor="32,10"
                iconURL="https://goo.gl/5y3S82"
                location="Melbourne+VIC"
            />
            </StaticGoogleMap>
        </div>
    );
}


export default SimpleMap;