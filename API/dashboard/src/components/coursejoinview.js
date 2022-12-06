import React from "react"

import Navbar from "./navbar"

import "../css/coursejoinview.css"

export default class CourseJoinView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            joinComplete: false,
            joinSuccess: false,
            errorFromServer: null,
        }

    }

    componentDidMount() {
        // mount is also called during authentication check, and
        // we need to make sure the join call is only made once.
        if (!this.state.hasOwnProperty('joinComplete')) {
            return;
        }

        if (!this.state.joinComplete) {
            const magicJoinKey = this.props.match.params.magic_join_key;
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                // Only run if the request is complete
                if (xhr.readyState !== 4) {
                    return;
                }
    
                if (xhr.status >= 200 && xhr.status < 300) {
                    let response = JSON.parse(xhr.responseText);
                    this.setState({
                        courseName: response.course_name,
                        joinComplete: true,
                        joinSuccess: true
                    });                
                } else {
                    let response = JSON.parse(xhr.responseText)
                    this.setState({
                        errorFromServer: response.error,
                        joinComplete: true,
                        joinSuccess: false
                    });
                }
            }.bind(this);
    
            xhr.open("POST", "/api/course/join");
            xhr.send(JSON.stringify({"magicJoinKey": magicJoinKey}));
        }
    }

    render() {
        let pageContent;
        if (this.state.joinComplete) {
            if (this.state.joinSuccess) {
                pageContent = <div>
                    <div>
                        <span className="title is-4">Enrollment Success</span>
                    </div>
                    <br></br>
                    <div>
                        <div>
                            <span className="has-text-success">You are successfully enrolled in {this.state.courseName}.</span>
                        </div>
                    </div>
                </div>;
            } else {
                pageContent = <div>
                    <div>
                        <span className="title is-4">Enrollment Failed</span>
                    </div>
                    <br></br>
                    <div>
                        <span>Enrollment failed with error:</span>
                        <div>
                            <span className="has-text-danger">{this.state.errorFromServer}</span>
                        </div>
                    </div>
                </div>
            }
        } else {
            pageContent = <div>
                <span>Enrolling...</span>
            </div>;
        }

        return (
            <div>
                <Navbar showLogin={false} history={this.props.history} />
                <div className="page-root">
                    <div className="course-join-root">
                        {pageContent}
                    </div>
                </div>
            </div>
        );
    }
}