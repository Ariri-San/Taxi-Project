import "./App.css";
import React, { Component } from "react";
import { ToastContainer } from "react-toastify";
import { Route, Routes } from "react-router";
import request from "./services/requestService";
import auth from "./services/authService";
import Navbar from "./components/navbar";
import Home from "./components/home";
import Register from "./components/register";
import Login from "./components/login";
import Logout from "./components/logout";
import Travel from "./components/travel";
import Travels from "./components/travels";
import TravelToHistory from "./components/travel_to_history";
import History from "./components/history";
import SimpleMap from "./components/map"
import Footer from "./components/footer";
import SimpleMap from './components/map';


class App extends Component {
  state = {};

  async componentDidMount() {
    try {
      const jwt = auth.getCurrentUser();
      const result = await request.getObjects("auth/users/", jwt.user_id);
      const is_admin = await request.saveObject({username: result.data.username}, "check_admin/")
      this.setState({
        user: {
          id: result.data.id,
          username: result.data.username,
          is_admin: is_admin.data,
        },
      });
    } catch (error) {}
  }

  render() {
    return (
      <React.Fragment>
        <ToastContainer />
        <Navbar user={this.state.user} />
        <div style={{marginBottom:"70px"}}>
          <Routes>
            <Route path="/" element={<Home />}></Route>
            <Route path="/map" element={<SimpleMap />}></Route>
            <Route path="/history" element={<History user={this.state.user} />}></Route>
            <Route path="/travel" element={<Travel user={this.state.user} />}></Route>
            <Route path="/travels" element={<Travels user={this.state.user} />}></Route>
            <Route path="/travel_to_history" element={<TravelToHistory user={this.state.user} />}></Route>
            <Route path="/register" element={<Register />}></Route>
            <Route path="/login" element={<Login />}></Route>
            <Route path="/logout" element={<Logout />}></Route>
          </Routes>
        </div>
        <Footer/>
      </React.Fragment>
    );
  }
}

export default App;
