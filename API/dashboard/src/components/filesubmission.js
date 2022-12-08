import React from "react"

import BuildHistory from "./buildhistory"
import Leaderboard from "./leaderboard"
import Navbar from "./navbar"

import "../css/projectview.css"

export default class Projectview extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            project: null,
        }
    }

    componentDidMount() {
        this.getProjectData();
    }

    getProjectData = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({project: response.project, loading: false});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, loading: false});
            }
        }.bind(this);
 
        xhr.open("GET", "/api/project?project_repo_id=" + this.props.match.params.project_repo_id);
        xhr.send();
    }

    render() {
        let pageContent;
        if (this.state.loading) {
            pageContent = <div>Loading...</div>
        } else {
            if (this.state.errorFromServer) {
                pageContent = <div className="project-root">
                    <span className="title is-4">Failed to retrieve project data</span>
                    <div>
                        <span className="has-text-danger">{this.state.errorFromServer}</span>
                    </div>
                </div>
            } else {
                let ownerText = this.state.project.has_metadata_fields && this.state.project.is_owner ? "You are the owner of this project" : "";
                let leaderboardContent = this.state.project.has_leaderboard ? (
                    <div>
                        <span>
                            <a href={"" + this.state.project.repo_id}>Leaderboard</a>
                        </span>
                    </div>) : (<div></div>);
                
                let fileSubmissionContent = this.state.project.has_required_files ? (
                    <div>
                        <span>
                            <a href={"/filesubmission/" + this.state.project.repo_id}>Submit File</a>
                        </span>
                    </div>) : (<div></div>);

                let autoRecContent = this.state.project.has_recommended_materials ? (
                    <div>
                        <span className="is-size-5 has-text-weight-bold	">Recommended Learning Materials</span>
                        {this.state.project.recommended_materials_links.map(courseLink => {
                            return (<div>
                                <br></br>
                                <span className="is-size-6 has-text-weight-semibold">{courseLink}</span>
                                <ul>
                                    {this.state.project.recommended_materials[courseLink].map(lessonName => {
                                        return <li className="list-item">{lessonName}</li>
                                    })}
                                </ul>
                            </div>)
                        })}
                    </div>
                ) : <div></div>

                pageContent = <div>
                    <div className="columns">
                        <div className="column is-one-third">
                            <div>
                                <span className="title is-4">{this.state.project.title}</span>
                            </div>
                            <div>
                                <span className="is-7 is-italic">{ownerText}</span>
                            </div>
                            <br></br>
                            <div>
                                <span><a href={this.state.project.hosting_url}>Github</a></span>
                            </div>
                            <div>
                                {fileSubmissionContent}
                            </div>
                            <div>
                                {leaderboardContent}
                            </div>
                            <br></br>
                            <div>
                                {autoRecContent}
                            </div>
                        </div>
                        <div className="column is-two-thirds">
                            <div className="build-history-wrapper">
                                <BuildHistory specificRepoId={this.state.project.repo_id} history={this.props.history} />
                            </div>
                        </div>
                    </div>
                </div>
            }
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