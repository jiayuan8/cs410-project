import React from "react"

import Project from "./project"

import "../css/projectlist.css"

/**
 * Makes an API request to our backend to get the project 
 * list for this user (or all projects if specified).
 */
export default class ProjectList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            projects: []
        }
    }

    componentDidMount() {
        this.getProjects();
    }

    getProjects = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({projects: response.projects});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);
 
        xhr.open("GET", this.props.projectListUrl);
        xhr.send();
    }

    renderProjects = () => {
        if (this.state.projects.length > 0) {
            let widthClass = this.props.isFullWidth ? "" : "is-one-third";
            return (
                    <div className="columns" style={{"flex-wrap": "wrap"}}>
                        {this.state.projects.map(project => {
                            return (
                                <div className={"column" + " " + widthClass}>
                                    <Project
                                        title={project.title}
                                        shortDescription={project.short_description}
                                        numLearners={project.num_learners}
                                        projectViewUrl={project.project_view_url}
                                    />
                                </div>
                            )
                        })}
                    </div>
            )
        } else {
            return (
                <div>
                    {this.props.projectListEmptyMsg}
                </div>
            )
        }
    }

    render() {
        return (
            <div>
                <p className="is-size-5 has-text-weight-bold">{this.props.projectListTitle}</p>
                {this.renderProjects()}
            </div>
        )
    }
}