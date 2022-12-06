import React from "react"

import Navbar from "./navbar"
import { PROJECT_CONST } from "./project";

export default class NewLeaderboardView extends React.Component {
    constructor(props) {
        super(props);
    
        this.state = {
            loading: true,
            ownedProjects: [],
            selectedProject: null,
            columns: [],
            rankingColumn: null,
            hideResults: false,
        }
    }

    componentDidMount() {
        this.getOwnedProjects();
    }

    getOwnedProjects = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                let projects = response.projects.filter(p => !p.has_leaderboard);
                if (projects.length == 0) {
                    this.setState({projects: projects, selectedProject: null, loading: false});
                } else {
                    this.setState({projects: projects, selectedProject: projects[0].title, loading: false});
                }
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, loading: false});
            }
        }.bind(this);
 
        xhr.open("GET", PROJECT_CONST.URL.LIST_OWNER);
        xhr.send();
    }

    addColumn = () => {
        let columns = this.state.columns;
        columns.push(this.state.newCol);

        if (columns.length == 1) {
            this.setState({
                columns: columns,
                rankingColumn: this.state.newCol,
                newCol: "",
            });        
        } else {
            this.setState({
                columns: columns,
                newCol: "",
            }); 
        }
    }

    removeColumn = (index) => {
        let columns = this.state.columns;
        let remCol = columns.splice(index, 1);

        if (columns.length == 0) {
            this.setState({columns: columns, rankingColumn: null});
        } else if (remCol == this.state.rankingColumn) {
            this.setState({columns: columns, rankingColumn: columns[0]});
        } else {
            this.setState({columns: columns});
        }
    }

    handleCheckboxChange = (event) => {
        this.setState({
            [event.target.id]: !this.state[event.target.id]
        })
    }

    handleSubmit = (e) => {
        e.preventDefault();

        const project = this.state.selectedProject;
        const columns = this.state.columns;
        const rankingColumn = this.state.rankingColumn;
        const hideResults = this.state.hideResults;

        if (project == null || columns == null || rankingColumn == null) {
            this.setState({errorFromServer: "Error: No fields can be left empty."});
            return;
        }

        this.setState({errorFromServer: null});

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                let leaderboardUrl = response.leaderboard_url;
                this.props.history.push(leaderboardUrl);
            } else {
                let response = JSON.parse(xhr.responseText);
                this.setState({errorFromServer: response.error});
            }
        }.bind(this);

        xhr.open("POST", "/api/project/leaderboard/new");
        xhr.send(JSON.stringify({
            project: project,
            columns: columns,
            rankingColumn: rankingColumn,
            hideResults: hideResults
        }));
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

    render() {
        let pageContent;
        if (this.state.loading) {
            pageContent = <div>Loading...</div>
        } else if (this.state.selectedProject != null) {
            pageContent = <div className="form-root">
                <div className="form-title">
                    <span className="title is-4">Create a New Leaderboard</span>
                </div>
                <div className="field">
                    {this.renderErrorMessage()}
                </div>
                <div className="field">
                    <div>
                        <label className="has-text-weight-semibold">Project</label>
                    </div>
                    <div className="select">
                        <select id="project" onChange={(e) => this.setState({selectedProject: e.target.value})}>
                            {this.state.projects.map(project => {
                                return (
                                    <option>{project.title}</option>
                                )
                            })}
                        </select>
                    </div>
                </div>
                <div className="field">
                    <label className="has-text-weight-semibold">Leaderboard Columns</label>
                    <div>
                        {this.state.columns.map((col, i) => {
                            return (
                                <div style={{"paddingBottom": "1%"}}>
                                    <button className="button is-danger is-light is-small" onClick={() => this.removeColumn(i)}>Remove</button>
                                    <span style={{"paddingLeft": "1%"}}>{col}</span>
                                </div>
                            )
                        })}
                    </div>
                    <br></br>
                    <div className="columns">
                        <div className="column">
                            <input className="input" id="columnName" placeholder="New Column Name" value={this.state.newCol} onChange={(e) => {this.setState({newCol: e.target.value})}} />
                        </div>
                        <div className="column">
                            <button className="button is-info" onClick={this.addColumn}>Add</button>
                        </div>
                    </div>
                </div>
                <div className="field">
                    <div>
                        <label className="has-text-weight-semibold">Ranking Column</label>
                    </div>
                    <div className="select">
                        <select id="rankingColumn" onChange={(e) => this.setState({rankingColumn: e.target.value})}>
                            {this.state.columns.map(col => {
                                return (
                                    <option>{col}</option>
                                )
                            })}
                        </select>
                    </div>
                </div>
                <div className="field">
                    <label className="checkbox">
                        <input id="hideResults" type="checkbox" onChange={this.handleCheckboxChange} />
                        &nbsp;Hide other users' leaderboard results
                    </label>
                </div>
                <div className="field">
                    <p className="control">
                        <button className="button is-success" onClick={this.handleSubmit}>Create</button>
                    </p>
                </div>
            </div>
        } else {
            pageContent = <div>You have no projects without leaderboards.</div>
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