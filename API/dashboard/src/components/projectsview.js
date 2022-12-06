import React from "react"

import ProjectList from "./projectlist"
import { PROJECT_CONST } from "./project"
import Navbar from "./navbar"

import "../css/projectsview.css"

export default class ProjectsView extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Navbar showLogin={false} history={this.props.history} />
                <div className="page-root">
                    <div className="background-box">
                        <ProjectList
                            projectListUrl={PROJECT_CONST.URL.LIST_USER}
                            projectListTitle={PROJECT_CONST.LIST_TITLE.USER}
                            projectListEmptyMsg={PROJECT_CONST.LIST_EMPTY_MSG.USER}
                            isFullWidth={false}
                        />
                    </div>
                    <div className="background-box">
                        <ProjectList
                            projectListUrl={PROJECT_CONST.URL.LIST_ALL}
                            projectListTitle={PROJECT_CONST.LIST_TITLE.ALL}
                            projectListEmptyMsg={PROJECT_CONST.LIST_EMPTY_MSG.ALL}
                            isFullWidth={false}
                        />
                    </div>
                </div>
            </div>
        )
    }
}