import React from "react"

import CourseList from "./courselist"
import { COURSE_CONST } from "./course"
import Navbar from "./navbar"

import "../css/coursesview.css"

export default class CoursesView extends React.Component {
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
                            courseListUrl={COURSE_CONST.URL.LIST_USER}
                            courseListTitle={COURSE_CONST.LIST_TITLE.USER}
                            courseListEmptyMsg={COURSE_CONST.LIST_EMPTY_MSG.USER}
                            isFullWidth={false}
                        />
                    </div>
                    <div className="background-box">
                        <CourseList
                            courseListUrl={COURSE_CONST.URL.LIST_ALL}
                            courseListTitle={COURSE_CONST.LIST_TITLE.ALL}
                            courseListEmptyMsg={COURSE_CONST.LIST_EMPTY_MSG.ALL}
                            isFullWidth={false}
                        />
                    </div>
                </div>
            </div>
        )
    }
}