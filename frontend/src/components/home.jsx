import React from "react";
import { Helmet } from "react-helmet";

function Home(props) {
    return(
        <div className="container">
            <Helmet>
                <title>Home</title>
            </Helmet>
            <h3>making us the preferred choice for both short and</h3>
            <br/>
            <p>
                extended trips.

                With Welwyn Airport Taxis, you can trust that
                <br/>
                you'll receive top-notch service from start to finish.
                <br/>
                Our drivers are professional, courteous, and
                <br/>
                knowledgeable about the best routes to ensure a
                <br/>
                smooth and enjoyable journey. Book your ride with
                <br/>
                us today and experience the convenience of
                <br/>
                traveling with Welwyn Airport Taxis.
            </p>
            <img src={require("../templates/img/photo_2024-03-07_14-09-14.jpg")} alt="" className="img-car"/>
            <p>
                If you prefer to speak with one of our
                <br/>
                representatives directly, feel free to give us a call or
                <br/>
                send us an email. We are available 24/7 to assist
                <br/>
                you with your booking and answer any questions
                <br/>
                you may have. Trust Welwyn Airport Taxis for all
                <br/>
                your transportation needs.
            </p>
        </div>
    );
}

export default Home;
