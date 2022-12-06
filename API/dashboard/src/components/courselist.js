import React from "react"

import Course from "./course"

import "../css/courselist.css"

/**
 * Makes an API request to our backend to get the course 
 * list for this user (or all courses if specified).
 */
export default class CourseList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            courses: []
        }
    }

    componentDidMount() {
        this.getCourses();
    }

    getCourses = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({courses: response.courses});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);
 
        xhr.open("GET", this.props.courseListUrl);
        xhr.send();
    }

    renderCourses = () => {
        if (this.state.courses.length > 0) {
            let widthClass = this.props.isFullWidth ? "" : "is-one-third";
            return (
                    <div className="columns" style={{"flex-wrap": "wrap"}}>
                        {this.state.courses.map(course => {
                            return (
                                <div className={"column" + " " + widthClass}>
                                    <Course
                                        name={course.name}
                                        shortDescription={course.short_description}
                                        numLearners={course.num_learners}
                                        courseUrl={course.course_url}
                                    />
                                </div>
                            )
                        })}
                    </div>
            )
        } else {
            return (
                <div>
                    {this.props.courseListEmptyMsg}
                </div>
            )
        }
    }

    render() {
        return (
            <div>
                <p className="is-size-5 has-text-weight-bold">{this.props.courseListTitle}</p>
                {this.renderCourses()}
            </div>
        )
    }
}