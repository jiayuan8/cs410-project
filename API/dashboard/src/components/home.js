import React from 'react';

import BuildHistory from "./buildhistory"
import LinkedAccount from "./linkedaccount"
import NewLinkedAccount from "./newlinkedaccount"
import ProjectList from './projectlist'
import Navbar from "./navbar"
import { PROJECT_CONST } from "./project"

import "../css/home.css"

export default class Home extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            linkedAccounts: [],
        }
    }

    componentDidMount() {
        this.getLinkedAccounts();
    }

    getLinkedAccounts = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({linkedAccounts: response.linked_accounts});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("GET", "/api/externalaccount/all");
        xhr.send();
    }

    renderPendingUploadContent = () => {
        if (this.state.pendingUploads.length === 0) {
            return (
                <span className="is-size-6">No pending uploads.</span>
            );
        } else {
            return (
                <div>
                    {this.state.pendingUploads.map(dataset => {
                        return (
                            <div>
                                <span className="is-size-6">{dataset.zip_path}</span>
                            </div>
                        );
                    })}
                </div>
            );
        }
    }

    render() {
        return (
            <div>
                <Navbar showLogin={false} history={this.props.history} />
                <div className="page-root">
                    <div className="columns">
                        <div className="column is-one-third">
                            <ProjectList
                                projectListUrl={PROJECT_CONST.URL.LIST_USER}
                                projectListTitle={PROJECT_CONST.LIST_TITLE.USER}
                                projectListEmptyMsg={PROJECT_CONST.LIST_EMPTY_MSG.USER}
                                isFullWidth={true}
                            />
                            <br></br>
                            <div>
                                <p className="is-size-5 has-text-weight-bold">Linked Acccounts</p>
                                {this.state.linkedAccounts.map(account => {
                                    return (
                                        <div className="linked-account-content-item" key={account.username + account.host_domain}>
                                            <LinkedAccount
                                                username={account.username}
                                                hostDomain={account.host_domain}
                                                linkedDate={account.linked_date}
                                            />
                                        </div>
                                    );
                                })}
                                <div className="linked-account-content-item">
                                    <NewLinkedAccount />
                                </div>
                            </div>
                        </div>
                        <div className="column is-two-thirds">
                            <BuildHistory history={this.props.history} />
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}