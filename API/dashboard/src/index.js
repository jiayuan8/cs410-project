import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import * as serviceWorker from './serviceWorker';
import { BrowserRouter as Router, Route, Redirect } from "react-router-dom";
import SignIn from "./components/signin"
import SignUp from "./components/signup"
import Home from "./components/home"
import BuildInfo from "./components/buildinfo"
import CourseView from "./components/courseview"
import CoursesView from "./components/coursesview"
import CourseJoinView from "./components/coursejoinview"
import ProjectsView from "./components/projectsview"
import ProjectView from "./components/projectview"
import FileSubmission from './components/filesubmission';
import ManageView from "./components/manageview"
import NewProjectView from "./components/newprojectview"
import NewCourseView from "./components/newcourseview"
import NewLeaderboardView from "./components/newleaderboardview"
import LeaderboardView from "./components/leaderboardview"
import { createBrowserHistory } from "history";

const history = createBrowserHistory()

const RequireAuth = (Component) => { 
    return class App extends Component { 
        constructor(props) {
            super(props);
            this.state = {authenticated: false, loading: true}
        }

        componentWillMount() { 
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                // Only run if the request is complete
                if (xhr.readyState !== 4) {
                    return;
                }

                if (xhr.status >= 200 && xhr.status < 300) {
                    let response = JSON.parse(xhr.responseText);
                    if (response.authenticated) {
                        this.setState({authenticated: true, loading: false});
                    } else {
                        this.setState({authenticated: false, loading: false});
                        return <Redirect to="/login" />
                    }
                } else {
                    this.setState({authenticated: false, loading: false});
                }
            }.bind(this);

            xhr.open("GET", "/api/login_status");
            xhr.send();
        }
 
        render() {
            if (this.state.loading) {
                return <h4>Loading...</h4>
            } else if (this.state.authenticated) {
                return <Component {...this.props} /> 
            } else {
                return <Redirect to="/login" />
            }
        }
    } 
}

ReactDOM.render(
    <Router history={history}>
        <Route path="/login" exact component={SignIn} />
        <Route path="/signup" exact component={SignUp} />
        <Route path="/" exact component={RequireAuth(Home)} />
        <Route path="/job/:job_id/:build_id" component={RequireAuth(BuildInfo)} />
        <Route path="/projects" component={RequireAuth(ProjectsView)} />
        <Route path="/manage" component={RequireAuth(ManageView)} />
        <Route path="/project/view/:project_repo_id" component={RequireAuth(ProjectView)} />
        <Route path="/project/filesubmission/:project_repo_id" component={RequireAuth(FileSubmission)} />
        <Route path="/project/new" component={RequireAuth(NewProjectView)} />
        <Route path="/course/view/:course_id" component={RequireAuth(CourseView)} />
        <Route path="/courses" component={RequireAuth(CoursesView)} />
        <Route path="/course/new" component={RequireAuth(NewCourseView)} />
        <Route path="/course/join/:magic_join_key" component={RequireAuth(CourseJoinView)} />
        <Route path="/leaderboard/new" component={RequireAuth(NewLeaderboardView)} />
        <Route path="/project/leaderboard/:project_repo_id" component={RequireAuth(LeaderboardView)} />
    </Router>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
