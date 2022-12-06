import React from "react"

import Navbar from "./navbar"
import ProjectList from "./projectlist"
import { PROJECT_CONST } from "./project"

export default class CourseView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            course: null,
        }
    }

    componentDidMount() {
        this.requestCourseData();
    }

    requestCourseData = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({course: response.course, loading: false});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, loading: false});
            }
        }.bind(this);
 
        xhr.open("GET", "/api/course?course_id=" + this.props.match.params.course_id);
        xhr.send();
    }

    render() {
        let pageContent;
        if (!this.state.loading) {
            if (this.state.course) {
                let learnerText = this.props.numLearners != 1 ? "learners" : "learner";
                let enrollmentLink = <div></div>;
                if (this.state.course.magic_join_url) {
                    enrollmentLink = <div>
                        Enrollment link:<br></br>
                        <a href={this.state.course.magic_join_url}>{this.state.course.magic_join_url}</a>
                    </div>
                }
                let ownerText = this.state.course.is_owner ? "You are the owner of this course" : "";

                pageContent = <div className="course-root">
                    <div>
                        <span className="title is-4">{this.state.course.name}</span>
                    </div>
                    <div>
                        <span className="is-7 is-italic">{ownerText}</span>
                    </div>
                    <br></br>
                    <div>
                        <span>{this.state.course.short_description}</span>
                    </div>
                    <br></br>
                    <div>
                        <span>Started by {this.state.course.num_learners} {learnerText}.</span>
                    </div>
                    <br></br>
                    {enrollmentLink}
                    <br></br>
                    <ProjectList 
                        projectListUrl={PROJECT_CONST.URL.LIST_COURSE + "?course_id=" + this.state.course._id}
                        projectListTitle={PROJECT_CONST.LIST_TITLE.COURSE}
                        projectListEmptyMsg={PROJECT_CONST.LIST_EMPTY_MSG.COURSE}
                        isFullWidth={false}
                    />
                </div>
            } else {
                pageContent = <div className="course-root">
                    <span className="title is-4">Failed to retrieve course data</span>
                    <div>
                        <span className="has-text-danger">{this.state.errorFromServer}</span>
                    </div>
                </div>
            }
        } else {
            pageContent = <div>
                <span>Loading course data...</span>
            </div>
        }

        return (
            <div>
                <Navbar showLogin={false} history={this.props.history} />
                <div className="page-root">
                    {pageContent}
                </div>
            </div>
        );
    }
}