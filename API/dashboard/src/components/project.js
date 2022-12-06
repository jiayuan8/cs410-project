import React from "react"

import "../css/project.css"

export const PROJECT_CONST = {
    URL: {
        LIST_ALL: "/api/project/list_all",
        LIST_USER: "/api/project/list_user",
        LIST_OWNER: "/api/project/list_owner",
        LIST_COURSE: "/api/project/list_course",
        CREATE: "/api/project/create",
    },
    LIST_TITLE: {
        ALL: "All Projects",
        USER: "Projects You've Started",
        OWNER: "Projects You Own",
        COURSE: "Projects in this Course",
    },
    LIST_EMPTY_MSG: {
        ALL: "There are no projects available.",
        USER: "You have not started any projects.",
        OWNER: "You do not own any projects.",
        COURSE: "This course does not have any projects.",
    }
}

export default class Project extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let learnerText = this.props.numLearners != 1 ? "learners" : "learner";

        return (
            <a href={this.props.projectViewUrl}>
                <div className="card project-card-root">
                    <div className="card-content">
                        <p className="title is-6">{this.props.title}</p>
                        <p className="subtitle is-7">Started by {this.props.numLearners} {learnerText}</p>
                        <p className="subtitle is-7">{this.props.shortDescription}</p>
                    </div>
                </div>
            </a>
        )
    }
}