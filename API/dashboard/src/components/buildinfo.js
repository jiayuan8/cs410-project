import React from "react"

import Navbar from "./navbar"
import "../css/buildinfo.css"

export default class BuildInfo extends React.Component {
    
    constructor(props) {
        super(props);

        this.state = {
            buildData: {git_url: "", build_number: ""},
            logLines: [],
        }
    }

    componentDidMount() {
        this.getBuildInfo();
        this.getBuildLogs();

        let infoInterval = setInterval(this.getBuildInfo, 1000);
        let logsInterval = setInterval(this.getBuildLogs, 1000);
        this.setState({infoInterval: infoInterval, logsInterval: logsInterval});
    }

    getBuildInfo = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);

                if (response.build_data.status === "SUCCESS" || response.build_data.status === "FAILURE") {
                    clearInterval(this.state.infoInterval);
                    clearInterval(this.state.logsInterval);
                }

                this.setState({buildData: response.build_data});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("GET", "/api/build?build_id=" + this.props.match.params.build_id);
        xhr.send();
    }

    getBuildLogs = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({logLines: response.build_logs});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("GET", "/api/build/logs?build_id=" + this.props.match.params.build_id);
        xhr.send();
    }
    
    msToHMS = (duration) => {
        let milliseconds = parseInt((duration%1000)/100)
            , seconds = parseInt((duration/1000)%60)
            , minutes = parseInt((duration/(1000*60))%60)
            , hours = parseInt((duration/(1000*60*60))%24);
    
        hours = (hours < 10) ? "0" + hours : hours;
        minutes = (minutes < 10) ? "0" + minutes : minutes;
        seconds = (seconds < 10) ? "0" + seconds : seconds;
    
        return hours + ":" + minutes + ":" + seconds + "." + milliseconds;
    }

    render() {
        return (
            <div>
                <Navbar showLogin={false} />
                <div className="page-root">
                    <div className="columns">
                        <div className="column is-one-third">
                            <div className="project-details-card">
                                <div className="card">
                                    <div className="card-content">
                                        <div className="project-details-title">
                                            <p className="title is-size-6">Project Details</p>
                                        </div>
                                        <div className="project-details-entry">
                                            <p className="is-size-6 has-text-weight-semibold">Git URL:</p>
                                            <p className="is-size-6">{this.state.buildData.git_url}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <div className="card">
                                    <div className="card-content">
                                        <div className="submission-details-title">
                                            <p className="title is-size-6">Submission Details</p>
                                        </div>
                                        <div className="submission-details-entry">
                                            <p className="is-size-6 has-text-weight-semibold">Submission Number:</p>
                                            <p className="is-size-6">{this.state.buildData.build_number}</p>
                                        </div>
                                        <div className="submission-details-entry">
                                            <p className="is-size-6 has-text-weight-semibold">Status:</p>
                                            <p className="is-size-6">{this.state.buildData.status}</p>
                                        </div>
                                        <div className="submission-details-entry">
                                            <p className="is-size-6 has-text-weight-semibold">Duration:</p>
                                            <p className="is-size-6">{this.msToHMS(this.state.buildData.time_elapsed)} (HH:MM:SS.MS)</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="column is-two-thirds">
                            <div className="card">
                                <div className="card-content">
                                    <div className="logs-title">
                                        <p className="title is-size-6">Submission Logs</p>
                                    </div>
                                    <div className="logs-div">
                                        <div className="log-lines">
                                            {this.state.logLines.map((line, index) => {
                                                return <p key={index} className="is-size-7">{line}</p>
                                            })}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}