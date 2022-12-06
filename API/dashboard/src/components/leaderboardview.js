import React from "react"

import Leaderboard from "./leaderboard"
import Navbar from "./navbar"

export default class LeaderboardView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            downloadUrl: null,
            exportInProgress: false
        }
    }

    componentDidMount() {
        this.getLeaderboardOwnershipStatus();
    }

    getLeaderboardOwnershipStatus = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({isOwner: response.is_owner, loading: false});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, loading: false});
            }
        }.bind(this);
 
        xhr.open("GET", "/api/project/leaderboard/ownership?project_repo_id=" + this.props.match.params.project_repo_id);
        xhr.send();
    }

    exportResults = () => {
        this.setState({exportInProgress: true});

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({downloadUrl: response.download_url, exportInProgress: false});
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, exportInProgress: false});
            }
        }.bind(this);
 
        xhr.open("GET", "/api/project/leaderboard/export?project_repo_id=" + this.props.match.params.project_repo_id);
        xhr.send();
    }

    render() {
        let pageContent;
        if (this.state.loading) {
            pageContent = <div>Loading...</div>
        } else if (this.state.isOwner) {
            let downloadLink = this.state.downloadUrl ? <div>
                <a href={this.state.downloadUrl} download>Click here to download the .csv file</a>
            </div> : <div></div>;
            let exportStatus = this.state.exportInProgress ? <div>
                <span>Leaderboard export currently being processed...</span>
            </div> : <div></div>;

            pageContent = <div className="columns">
                <div className="column is-one-quarter">
                    <button className="button is-info" onClick={this.exportResults}>Export Leaderboard Results</button>
                    {exportStatus}
                    {downloadLink}
                </div>
                <div className="column is-three-quarters">
                    <Leaderboard projectRepoId={this.props.match.params.project_repo_id} />
                </div>
            </div>
        } else {
            pageContent = <Leaderboard projectRepoId={this.props.match.params.project_repo_id} />;
        }

        return (
            <div>
                <Navbar showLogin={false} />
                <div className="page-root">
                    {pageContent}
                </div>
            </div>
        )
    }
}