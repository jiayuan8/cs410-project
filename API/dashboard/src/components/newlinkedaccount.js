import React from "react"

export default class NewLinkedAccount extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            username: "",
            hostDomain: "",
            apiKey: "",
            showLinkNewAccount: false,
            errorFromServer: null,
        }
    }

    handleChange = (event) => {
        this.setState({
          [event.target.id]: event.target.value
        });
    }

    handleLink = (event) => {
        event.preventDefault();

        this.setState({errorFromServer: null});

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                window.location.reload();
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("POST", "/api/externalaccount/link");
        xhr.setRequestHeader('Content-type', 'application/json');
        xhr.send(JSON.stringify({
            username: this.state.username,
            hostDomain: this.state.hostDomain,
            apiKey: this.state.apiKey,
        }));
    }

    renderAccountLinkError = () => {
        if (this.state.errorFromServer) {
            return (
                <div>
                    <span className="has-text-danger">{this.state.errorFromServer}</span>
                </div>
            );
        }
    }

    renderNewAccountLink = () => {
        if (this.state.showLinkNewAccount) {
            return (
                <div className="card">
                    <div className="card-content">
                        <div className="field">
                            <label class="label">Host Domain</label>
                            <div className="control">
                                <input id="hostDomain" className="input" type="text" placeholder="e.g., github.com" onChange={this.handleChange} />
                            </div>
                        </div>
                        <div className="field">
                            <label class="label">Host Domain Username</label>
                            <div className="control">
                                <input id="username" className="input" type="text" placeholder="Username" onChange={this.handleChange} />
                            </div>
                        </div>
                        <div className="field">
                            <label class="label">API Key</label>
                            <div className="control">
                                <input id="apiKey" className="input" type="password" placeholder="API Key" onChange={this.handleChange} />
                            </div>
                        </div>
                        <div className="field is-grouped">
                            <p className="control">
                                <a className="button is-light" onClick={() => this.setState({showLinkNewAccount: false})}>
                                    Cancel
                                </a>
                            </p>
                            <p className="control">
                                <a className="button is-primary" onClick={this.handleLink}>
                                    Link
                                </a>
                            </p>
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <a className="button is-primary"
                   onClick={() => this.setState({showLinkNewAccount: true})}
                >
                    Link new account
                </a>
            );
        }
    }

    render() {
        return (
            <div>
                {this.renderAccountLinkError()}
                {this.renderNewAccountLink()}
            </div>
        );
    }
}