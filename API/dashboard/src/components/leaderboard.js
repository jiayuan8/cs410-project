import React from "react"

export default class Leaderboard extends React.Component {
    constructor(props) {
        super(props);
    
        this.state = {
            loading: true,
            columnNames: [],
            rows: []
        }
    }

    componentDidMount() {
        this.getLeaderboardData();
    }

    getLeaderboardData = () => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            // Only run if the request is complete
            if (xhr.readyState !== 4) {
                return;
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                let response = JSON.parse(xhr.responseText);
                this.setState({
                    columnNames: response.columns,
                    rows: response.rows,
                    leaderboardId: response.leaderboard_id,
                    loading: false,
                });                
            } else {
                let response = JSON.parse(xhr.responseText)
                this.setState({errorFromServer: response.error, loading: false});
            }
        }.bind(this);
 
        xhr.open("GET", "/api/project/leaderboard?project_repo_id=" + this.props.projectRepoId);
        xhr.send();
    }

    render() {
        return (
            <div>
                <h5>Leaderboard ID: {this.state.leaderboardId}</h5>
                <table className="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Username</th>
                            <th>Submission Number</th>
                            {this.state.columnNames.map(col => {
                                return <th>{col}</th>
                            })}
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.rows.map(row => {
                            return (
                                <tr>
                                    <th>{row.rank}</th>
                                    <th>{row.username}</th>
                                    <th>{row.submission_number}</th>
                                    {row.data.map(field => {
                                        return <td>{field}</td>
                                    })}
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        );
    }
}