import React from "react"

import BuildItem from "./builditem"

import "../css/buildhistory.css"

export default class BuildHistory extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            buildHistory: [],
            activeFilterText: "No Filter",
            activeFilterVar: null,
            activeFilterValue: null,
            buildFilters: [
                {
                    filterText: "No Filter",
                    filterVar: null,
                    filterValue: ""
                },
                {
                    filterText: "Git URL",
                    filterVar: "git_url",
                    filterValue: ""
                },
                {
                    filterText: "Created Date",
                    filterVar: "build_time",
                    filterValue: ""
                },
                {
                    filterText: "Success",
                    filterVar: "build_status",
                    filterValue: "SUCCESS"
                },
                {
                    filterText: "Failure",
                    filterVar: "build_status",
                    filterValue: "FAILURE"
                }
            ]
        }
    }

    componentDidMount() {
        this.getBuildHistory();
    }

    getBuildHistory = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({buildHistory: response.build_items, loading: false});                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, loading: false});
            }
        }.bind(this);

        let url = "/api/build/history";
        if (this.props.specificRepoId) {
            url += "?repo_id=" + this.props.specificRepoId
        }

        xhr.open("GET", url);
        xhr.send();
    }

    setFilter = (filter) => {
        this.setState({
            activeFilterText: filter.filterText,
            activeFilterVar: filter.filterVar,
            activeFilterValue: filter.filterValue
        });
    }

    handleFilterValue = (event) => {
        this.setState({activeFilterValue: event.target.value});
    }

    renderBuildHistory = () => {
        let buildHistory = this.state.buildHistory;
        
        if (this.state.activeFilterVar !== null &&
            this.state.activeFilterValue !== null &&
            this.state.activeFilterValue.length > 0) {
                buildHistory = buildHistory.filter(buildItem => {
                    if (this.state.activeFilterVar === "build_time") {
                        let buildDate = new Date(buildItem[this.state.activeFilterVar] * 1000);
                        return buildDate.toLocaleDateString() === this.state.activeFilterValue
                    } else {
                        return buildItem[this.state.activeFilterVar] === this.state.activeFilterValue
                    }
                });
        }

        if (buildHistory.length > 0) {
            return (
                <div>
                    {buildHistory.map(build => {
                        return (
                            <div key={build.build_id} className="build-history-item">
                                <BuildItem buildData={build} history={this.props.history} />
                            </div>
                        );
                    })}
                </div>
            );
        } else {
            return (
                <div>
                    <p className="is-size-6">No submissions are available or match the filter.</p>
                </div>
            );
        }
    }

    render() {
        let historyContent;
        if (this.state.loading) {
            historyContent = <div>Loading submission history...</div>
        } else {
            if (this.state.errorFromServer) {
                historyContent = <div>
                    <span className="title is-4">Failed to retrieve submission history</span>
                    <div>
                        <span className="has-text-danger">{this.state.errorFromServer}</span>
                    </div>
                </div>
            } else {
                historyContent = <div>
                    <div className="build-items">
                        {this.renderBuildHistory()}
                    </div>
                </div>
            }
        }
        return (
            <div>
                <div className="columns">
                    <div className="column is-one-third">
                        <div className="build-history-title">
                            <p className="is-size-5 has-text-weight-bold">Submission History</p>
                        </div>
                    </div>
                    <div className="column is-two-thirds">
                        <div className="build-history-filter">
                            <div className="field has-addons has-addons-right">
                                <div className="control">
                                    <div className="dropdown is-hoverable">
                                        <div className="dropdown-trigger">
                                            <button className="button" aria-haspopup="true" aria-controls="dropdown-menu">
                                            <span>{this.state.activeFilterText}</span>
                                                <span className="icon is-small">
                                                    <i className="fas fa-angle-down" aria-hidden="true"></i>
                                                </span>
                                            </button>
                                        </div>
                                        <div className="dropdown-menu" id="dropdown-menu" role="menu">
                                            <div className="dropdown-content">
                                                {this.state.buildFilters.map(filter => {
                                                    return (
                                                        <a className="dropdown-item" onClick={() => this.setFilter(filter)}>
                                                            {filter.filterText}
                                                        </a>
                                                    );
                                                })}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="control is-expanded">
                                    <input
                                        className="input is-fullwidth"
                                        type="text"
                                        placeholder="Filter value"
                                        value={this.activeFilterValue}
                                        onChange={this.handleFilterValue}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="build-items">
                    {historyContent}
                </div>
            </div>
        );
    }
}