import React from 'react';
import "../css/signin.css"

export default class SignIn extends React.Component {
    constructor(props) {
        super(props);
    
        this.state = {
            email: "",
            password: "",
        };
    }

    handleChange = (event) => {
        this.setState({
          [event.target.id]: event.target.value
        });
    }
    
    handleSubmit = (event) => {
        event.preventDefault();

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                this.setState({errorFromServer: null});
                this.props.history.push("/");
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("POST", "/api/login");
        xhr.setRequestHeader('Content-type', 'application/json');
        xhr.send(JSON.stringify({
            email: this.state.email,
            password: this.state.password,
        }));
    }

    renderErrorMessage = () => {
        if (this.state.errorFromServer) {
            return (
                <div>
                    <span className="has-text-danger">{this.state.errorFromServer}</span>
                </div>
            );
        } else {
            return <div></div>;
        }
    }

    render() {
        return (
            <div id="signin-root">
                <div id="signin-title">
                    <span className="title is-4">LiveDataLab</span>
                </div>
                <div className="field">
                    <span>Need an account? <a href="/signup">Sign up here</a></span>
                </div>
                <div className="field">
                    {this.renderErrorMessage()}
                </div>
                <div className="field">
                <p className="control has-icons-left has-icons-right">
                    <input className="input" id="email" type="email" placeholder="Email" onChange={this.handleChange} />
                    <span className="icon is-small is-left">
                        <i className="fas fa-envelope"></i>
                    </span>
                    <span className="icon is-small is-right">
                        <i className="fas fa-check"></i>
                    </span>
                </p>
                </div>
                <div className="field">
                <p className="control has-icons-left">
                    <input className="input" id="password" type="password" placeholder="Password" onChange={this.handleChange} />
                    <span className="icon is-small is-left">
                        <i className="fas fa-lock"></i>
                    </span>
                </p>
                </div>
                <div className="field">
                <p className="control">
                    <button className="button is-success" onClick={this.handleSubmit}>Sign In</button>
                </p>
                </div>
            </div>
        );
    }
}