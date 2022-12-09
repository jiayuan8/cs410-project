import React from "react"

import BuildHistory from "./buildhistory"
import Leaderboard from "./leaderboard"
import Navbar from "./navbar"

import "../css/projectview.css"

export default class FileSubmission extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            project: null,
            errorFromServer: null,
        }
    }

    componentDidMount() {
        this.getProjectData();
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

    updateFileSelected = (event, index) => {
        if (event.target.files.length > 0) {
            let file = event.target.files[0];
            let filepath = this.state.project.required_files[index].filepath
            let filename = this.state.project.required_files[index].filename
            
            if (file.name !== filename) {
                event.target.value = null
                return 
            }

            this.state.fileSubmitted[index].fileName = filename
            this.state.fileSubmitted[index].filePath = filepath
            this.state.fileSubmitted[index].fileContent = file
            console.log(this.state.project)
        } else {
            this.state.fileSubmitted[index].fileContent = null
        }
    }

    handleSubmit = () => {

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

            this.setState({fileSubmitted: Array(this.state.project.required_files.length).fill({
                filePath: null,
                fileName: null,
                fileContent: null
            })})
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
                            <div className="field">
                                {this.renderErrorMessage()}
                            </div>

                            <div className="file-submission-wrapper">
                                {this.state.project.required_files.map((fileInfo, index) => {
                                    return (
                                        <div key={index}>
                                            <label className="has-text-weight-semibold">{fileInfo.filename}</label>
                                            <input className="input" type="file" accept={fileInfo.filename} onChange={e => this.updateFileSelected(e, index)}/>
                                        </div>
                                    )
                                })}
                            </div>

                            <div className="field">
                                <p className="control">
                                    <button className="button is-success" onClick={this.handleSubmit}>Submit Files</button>
                                </p>
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