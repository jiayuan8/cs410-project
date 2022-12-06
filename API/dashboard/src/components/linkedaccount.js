import React from "react"

import "../css/linkedaccount.css"

export default class LinkedAccount extends React.Component {
    render() {
        return (
            <div className="card">
                <div className="linked-account-content">
                    <div className="level">
                        <div className="level-left">
                            <div className="level-item">
                                <p className="title is-6">{this.props.username}</p>    
                            </div>
                            <div className="level-item">
                                <p className="is-6">{this.props.hostDomain}</p>
                            </div>
                        </div>
                    </div>
                    <p className="subtitle is-7 is-italic">Linked on: {this.props.linkedDate}</p>
                </div>
            </div>
        );
    }
}