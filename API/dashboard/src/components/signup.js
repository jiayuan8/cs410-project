import React from 'react';
import "../css/signup.css"

export default class SignUp extends React.Component {
    constructor(props) {
        super(props);
    
        this.state = {
            email: "",
            username: "",
            password: "",
            confirmedPassword: "",
            errorFromServer: null,
        };
    }

    handleChange = (event) => {
        this.setState({
          [event.target.id]: event.target.value
        });
      }
    
    handleSubmit = (event) => {
        event.preventDefault();

        if (this.state.password !== this.state.confirmedPassword) {
            this.setState({passwordMismatch: true});
            return;
        } else {
            this.setState({passwordMismatch: false});
        }

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

        xhr.open("POST", "/api/signup");
        xhr.setRequestHeader('Content-type', 'application/json');
        xhr.send(JSON.stringify({
            email: this.state.email,
            username: this.state.username,
            password: this.state.password,
            confirmedPassword: this.state.confirmedPassword,
        }));
    }

    renderErrorMessage = () => {
        if (this.state.passwordMismatch) {
            return (
                <div>
                    <span className="has-text-danger">Passwords do not match.</span>
                </div>
            );
        } else if (this.state.errorFromServer) {
            return (
                <div>
                    <span className="has-text-danger">{this.state.errorFromServer}</span>
                </div>
            );
        }
    }

    render() {
        return (
            <div id="signup-root">
                <div id="signup-title">
                    <span className="title is-4">LiveDataLab</span>
                </div>
                <div className="field">
                    <span>Already have an account? <a href="/login">Sign in here</a></span>
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
                <p className="control">
                    <input className="input" id="username" placeholder="Username" onChange={this.handleChange} />
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
                <p className="control has-icons-left">
                    <input className="input" id="confirmedPassword" type="password" placeholder="Confirm password" onChange={this.handleChange} />
                    <span className="icon is-small is-left">
                        <i className="fas fa-lock"></i>
                    </span>
                </p>
                </div>
                <div className="field">
                <p className="control">
                    <button className="button is-success" onClick={this.handleSubmit}>Sign Up</button>
                </p>
                </div>
            </div>
        );
    }
}