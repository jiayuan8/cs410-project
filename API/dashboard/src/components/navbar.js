import React from "react"

import livedataLogo from "../img/livedata-logo.png"

export default class Navbar extends React.Component {
    constructor(props) {
        super(props);
    }

    getAuthText = () => {
        return this.props.showLogin ? "Log in" : "Log out"
    }

    getAuthRoute = () => {
        return this.props.showLogin ? "/login" : "/logout"
    }

    handleAuthAction = () => {
        if (this.props.showLogin) {
            this.handleLogin();
        } else {
            this.handleLogout();
        }
    }

    handleLogin = () => {
        this.props.history.push("/login");
    }

    handleLogout = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                this.props.history.push("/login");           
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("GET", "/api/logout");
        xhr.send();
    }

    handleDeleteLinks = () => {
         var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
            }
                else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("GET", "/api/externalaccount/deleteall");
        xhr.send();
    }

    render() {
        return (
            <nav className="navbar" role="navigation" aria-label="main navigation">
                <div className="navbar-brand">
                    <img src={livedataLogo} width="112" height="28" />
                </div>

                <div id="navbarBasicExample" className="navbar-menu">
                    <div className="navbar-start">
                        <a className="navbar-item" href="/">
                            Home
                        </a>
                        <a className="navbar-item" href="/projects">
                            Projects
                        </a>
                        <a className="navbar-item" href="/courses">
                            Courses
                        </a>
                        <a className="navbar-item" href="/manage">
                            Manage
                        </a>

                        <div className="navbar-item has-dropdown is-hoverable">
                            <a className="navbar-link">
                                Create
                            </a>
                            <div className="navbar-dropdown">
                                <a className="navbar-item" href="/project/new">
                                    Project
                                </a>
                                <a className="navbar-item" href="/course/new">
                                    Course
                                </a>
                                <a className="navbar-item" href="/leaderboard/new">
                                    Leaderboard
                                </a>
                            </div>
                        </div>
                    </div>
                    <div className="navbar-end">
                     <a className="navbar-item" onClick={this.handleDeleteLinks}>
                        Delete Linked Accounts
                        </a>
                        <a className="navbar-item" onClick={this.handleAuthAction}>
                            {this.getAuthText()}
                        </a>
                    </div>
                </div>
            </nav>
        )
    }
}