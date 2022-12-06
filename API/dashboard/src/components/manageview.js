import React from "react"

import Navbar from "./navbar"

import CourseList from "./courselist"
import { COURSE_CONST } from "./course"

import ProjectList from "./projectlist"
import { PROJECT_CONST } from "./project"

// import "../css/manageview.css"

export default class ManageView extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Navbar showLogin={false} history={this.props.history} />
                <div className="page-root">
                    <div className="background-box">
                        <CourseList 
                            courseListUrl={COURSE_CONST.URL.LIST_OWNER}
                            courseListTitle={COURSE_CONST.LIST_TITLE.OWNER}
                            courseListEmptyMsg={COURSE_CONST.LIST_EMPTY_MSG.OWNER}
                            isFullWidth={false}
                        />
                        <br></br>
                        <ProjectList
                            projectListUrl={PROJECT_CONST.URL.LIST_OWNER}
                            projectListTitle={PROJECT_CONST.LIST_TITLE.OWNER}
                            projectListEmptyMsg={PROJECT_CONST.LIST_EMPTY_MSG.OWNER}
                            isFullWidth={false}
                        />
                    </div>
                </div>
            </div>
        )
    }
}