import React from "react"

import "../css/builditem.css"

export default class BuildItem extends React.Component {
    formatDate = (buildTime) => {
        let date = new Date(buildTime * 1000);
        return date.toLocaleString();
    }

    redirecToBuildInfo = () => {
        const buildURL = "/job/" + this.props.buildData.job_id + "/" + this.props.buildData.build_id
        this.props.history.push(buildURL)
    }

    copyGitURL = (event) => {
        // prevent onclick of full build item div
        event.cancelBubble = true;
        if (event.stopPropagation) {
            event.stopPropagation();
        }

        const tempElement = document.createElement('textarea');
        tempElement.value = this.props.buildData.git_url;
        document.body.appendChild(tempElement);
        tempElement.select();
        document.execCommand('copy');
        document.body.removeChild(tempElement);
    }

    backgroundColor = () => {
        if (this.props.buildData.build_status === "FAILURE") {
            return "hsla(14, 100%, 53%, 0.2)";
        } else if (this.props.buildData.build_status === "SUCCESS") {
            return "hsla(120, 73%, 75%, 0.2)";
        }
    }

    render() {
        return (
            <div className="card" onClick={this.redirecToBuildInfo}>
                <div className="build-item-content" style={{"background-color": this.backgroundColor()}}>
                    <div className="level">
                        <div className="level-left">
                            <div className="level-item">
                                <p id={this.props.buildData.build_id} className="title is-size-7">{this.props.buildData.git_url}</p>
                            </div>
                            <div className="level-item">
                                <p className="is-size-7">Submission Number: {this.props.buildData.build_number}</p>
                            </div>
                            <div className="level-item">
                                <p className="is-size-7">({this.formatDate(this.props.buildData.build_time)})</p>
                            </div>
                        </div>
                        <div className="level-right">
                            <div className="level-item">
                                <div className="copy-git-url-div" onClick={this.copyGitURL}>
                                    <p className="is-size-7">Copy Git URL</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}