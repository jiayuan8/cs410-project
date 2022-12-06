import React from "react"

import "../css/course.css"

export const COURSE_CONST = {
    URL: {
        LIST_ALL: "/api/course/list_all",
        LIST_USER: "/api/course/list_user",
        LIST_OWNER: "/api/course/list_owner",
        CREATE: "/api/course/create",
    },
    LIST_TITLE: {
        ALL: "All Courses",
        USER: "Courses You're Enrolled In",
        OWNER: "Courses You Own",
    },
    LIST_EMPTY_MSG: {
        ALL: "There are no courses available.",
        USER: "You are not enrolled in any courses.",
        OWNER: "You do not own any courses.",
    }
}

export default class Course extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let learnerText = this.props.numLearners != 1 ? "learners" : "learner";

        return (
            <a href={this.props.courseUrl}>
                <div className="card course-card-root">
                    <div className="card-content">
                        <p className="title is-6">{this.props.name}</p>
                        <p className="subtitle is-7">Started by {this.props.numLearners} {learnerText}</p>
                        <p className="subtitle is-7">{this.props.shortDescription}</p>
                    </div>
                </div>
            </a>
        )
    }
}