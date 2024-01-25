import "./App.css";
import React, { Component } from "react";
import { ToastContainer } from "react-toastify";
import { Route, Routes } from "react-router";
import request from "./services/requestService";
import auth from "./services/authService";
import SimpleMap from "./components/map";

class App extends Component {
  state = {};

  async componentDidMount() {
    try {
      const jwt = auth.getCurrentUser();
      const result = await request.getObjects("auth/users/", jwt.user_id);
      this.setState({
        user: {
          id: result.data.id,
          username: result.data.username,
        },
      });
    } catch (error) {}
  }

  render() {
    return (
      <React.Fragment>
        <ToastContainer />
        <Navbar user={this.state.user} />
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/users" element={<Customers />}></Route>
          <Route
            path="/users/:id"
            element={this.state.user && <Userr user={this.state.user} />}
          ></Route>
          <Route path="/travels" element={<Travels user={this.state.user} />}></Route>
          <Route path="/travels/:id" element={<Travel user={this.state.user} />}></Route>
          <Route path="/login" element={<Login />}></Route>
          <Route path="/logout" element={<Logout />}></Route>
        </Routes>
        <SimpleMap></SimpleMap>
      </React.Fragment>
    );
  }
}

export default App;
