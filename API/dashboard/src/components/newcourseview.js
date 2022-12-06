import React from "react"

import Navbar from "./navbar"

import "../css/newcourseview.css"

export default class NewCourseView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            errorFromServer: null,
            courseName: null,
            shortDescription: null,
            magicJoinUrl: null,
            courseCreated: false,
            isPublic: false,
        }
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

    handleChange = (event) => {
        this.setState({
          [event.target.id]: event.target.value
        });
    }

    handleCheckboxChange = (event) => {
        this.setState({
            [event.target.id]: !this.state[event.target.id]
        })
    }

    handleSubmit = (event) => {
        event.preventDefault();

        const courseName = this.state.courseName;
        const courseShortDescription = this.state.shortDescription;
        const isCoursePublic = this.state.isPublic;

        if (courseName == null || courseShortDescription == null) {
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
                this.setState({magicJoinUrl: response.magic_join_url, courseCreated: true});
            } else {
                let response = JSON.parse(xhr.responseText);
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        let payload = {
            courseName: courseName,
            courseShortDescription: courseShortDescription,
            isCoursePublic: isCoursePublic,
        }

        xhr.open("POST", "/api/course/create");
        xhr.send(JSON.stringify(payload));
    }

    render() {
        let pageContent;
        if (this.state.courseCreated) {
            pageContent = (<div className="form-root">
                <div>
                    <span className="title is-4">Course Successfully Created!</span>
                </div>
                <div>
                    <span>
                        Users can enroll in your course by visiting the following link:<br></br>
                        <a href={this.state.magicJoinUrl}>{this.state.magicJoinUrl}</a>
                    </span>
                </div>
            </div>
            )
        } else {
            pageContent = (<div className="form-root">
                <div className="form-title">
                    <span className="title is-4">Create a New Course</span>
                </div>
                <div className="field">
                    {this.renderErrorMessage()}
                </div>
                <div className="field">
                    <input className="input" id="courseName" placeholder="Course Name" onChange={this.handleChange} />
                </div>
                <div className="field">
                    <input className="input" id="shortDescription" placeholder="Short Description" onChange={this.handleChange} />
                </div>
                <div className="field">
                    <label className="checkbox">
                        <input id="isPublic" type="checkbox" onChange={this.handleCheckboxChange} />
                        &nbsp;Make Course Available to Public
                    </label>
                </div>
                <div className="field">
                    <p className="control">
                        <button className="button is-success" onClick={this.handleSubmit}>Create</button>
                    </p>
                </div>
            </div>)
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