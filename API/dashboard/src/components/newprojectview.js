import React from "react"

import { PROJECT_CONST }  from "./project"
import { COURSE_CONST } from "./course"
import Navbar from "./navbar"

import "../css/newprojectview.css"

export default class NewProjectView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            errorFromServer: null,
            projectName: null,
            shortDescription: null,
            projectZipFile: null,
            projectReadme: null,
            projectCourse: null,
            autoRecommendMaterials: false,
            requiredFiles: []
        }
    }

    componentDidMount() {
        this.loadOwnedCourses();
    }

    loadOwnedCourses = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({courses: response.courses, loading: false});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, loading: false});
            }
        }.bind(this);
 
        xhr.open("GET", COURSE_CONST.URL.LIST_OWNER);
        xhr.send();
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

    addFormFields() {
        this.setState(({
            requiredFiles: [...this.state.requiredFiles, { filepath: "", filename: "" }]
        }))
    }

    removeFormFields(i) {
        let requiredFiles = this.state.requiredFiles;
        requiredFiles.splice(i, 1);
        this.setState({ requiredFiles });
    }

    handleChange = (event) => {
        this.setState({
          [event.target.id]: event.target.value
        });
    }

    handleRequiredFileChange(i, e) {
        let requiredFiles = this.state.requiredFiles;
        requiredFiles[i][e.target.name] = e.target.value;
        this.setState({ requiredFiles });
    }

    zipFileSelected = (event) => {
        if (event.target.files.length > 0) {
            let file = event.target.files[0];
            this.setState({projectZipFile: file});
        } else {
            this.setState({projectZipFile: null});
        }
    }

    readmeFileSelected = (event) => {
        if (event.target.files.length > 0) {
            let file = event.target.files[0];
            this.setState({projectReadme: file});
        } else {
            this.setState({projectReadme: null});
        }
    }

    courseSelected = (event) => {
        if (event.target.value === "None") {
            this.setState({projectCourse: null});
        } else {
            this.setState({projectCourse: event.target.value});
        }
    }

    handleCheckboxChange = (event) => {
        this.setState({
            [event.target.id]: !this.state[event.target.id]
        })
    }

    handleSubmit = (event) => {
        event.preventDefault();

        const projectName = this.state.projectName;
        const projectShortDescription = this.state.shortDescription;
        const projectReadme = this.state.projectReadme;
        const projectZipFile = this.state.projectZipFile;
        const projectCourse = this.state.projectCourse;
        const autoRecommendMaterials = this.state.autoRecommendMaterials;
        const requiredFiles = JSON.stringify(this.state.requiredFiles.filter(element => {return element.filename !== ''}));

        if (projectName == null || projectShortDescription == null || projectReadme == null || projectZipFile == null) {
            this.setState({errorFromServer: "Error: No fields can be left empty."});
            return;
        }

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                let projectUrl = response.project_url;
                this.props.history.push(projectUrl);
            } else {
                let response = JSON.parse(xhr.responseText);
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        let formData = new FormData();
        formData.append("project_readme", projectReadme);
        formData.append("project_zipfile", projectZipFile);
        formData.append("projectName", projectName);
        formData.append("projectShortDescription", projectShortDescription);
        formData.append("projectCourse", projectCourse);
        formData.append("autoRecommendMaterials", autoRecommendMaterials);
        formData.append("requiredFiles", requiredFiles);

        xhr.open("POST", PROJECT_CONST.URL.CREATE);
        xhr.send(formData);
    }

    render() {
        let pageContent;
        if (this.state.loading) {
            pageContent = <div>
                <span>Loading...</span>
            </div>
        } else {
            pageContent = <div className="form-root">
                <div className="form-title">
                    <span className="title is-4">Create New Project</span>
                </div>
                <div className="field">
                    {this.renderErrorMessage()}
                </div>
                <div className="field">
                    <input className="input" id="projectName" placeholder="Project Name" onChange={this.handleChange} />
                </div>
                <div className="field">
                    <input className="input" id="shortDescription" placeholder="Short Description" onChange={this.handleChange} />
                </div>
                <div className="field">
                    <div>
                        <label className="has-text-weight-semibold">Project README</label>
                    </div>
                    <input className="input" type="file" accept=".md" onChange={this.readmeFileSelected} />
                </div>
                <div className="field">
                    <div>
                        <label className="has-text-weight-semibold">Project Starter Files (.zip only)</label>
                    </div>
                    <input className="input" type="file" accept=".zip" onChange={this.zipFileSelected} />
                </div>
                <div className="field">
                    <div>
                        <label className="has-text-weight-semibold">Course (optional)</label>
                    </div>
                    <div className="select">
                        <select id="projectCourse" onChange={this.courseSelected}>
                            <option>None</option>
                            {this.state.courses.map(course => {
                                return (
                                    <option>{course.name}</option>
                                )
                            })}
                        </select>
                    </div>
                </div>

                <div className="field">
                    <div>
                        <label className="has-text-weight-semibold">Required Files for Grading</label>
                    </div>
                    {this.state.requiredFiles.map((element, index) => (
                        <div className="form-inline" key={index}>
                            <label>Path</label>
                            <input className="input" type="text" name="filepath" placeholder="Default is project root directory" value={element.filepath || ""} onChange={e => this.handleRequiredFileChange(index, e)} />
                            <label>File Name</label>
                            <input className="input" type="text" name="filename" placeholder="i.e. two_sum.py" value={element.filename || ""} onChange={e => this.handleRequiredFileChange(index, e)} />
                            <button type="button"  className="button remove" onClick={() => this.removeFormFields(index)}>Remove</button>
                        </div>
                      ))}
                    <div className="button-section">
                      <button className="button add" type="button" onClick={() => this.addFormFields()}>Add</button>
                    </div>
                </div>

                <div className="field">
                    <label className="checkbox">
                        <input id="autoRecommendMaterials" type="checkbox" onChange={this.handleCheckboxChange} />
                        &nbsp;Auto-Recommend Learning Materials
                    </label>
                </div>
                <div className="field">
                    <p className="control">
                        <button className="button is-success" onClick={this.handleSubmit}>Create</button>
                    </p>
                </div>
            </div>
        }
        return (
            <div>
                <Navbar showLogin={false} history={this.props.history} />
                <div className="page-root">
                    {pageContent}
                </div>
            </div>
        )
    }
}