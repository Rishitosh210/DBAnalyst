import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import axios from 'axios'
import { Route, Switch , BrowserRouter as Router } from 'react-router-dom';
import * as serviceWorker from './serviceWorker';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


const routing = (
  <Router>
    <div>
        <Switch>
      <Route  exact path="/" component={App} />
      {/*<Route path="/users" component={Users} />*/}
      {/*<Route path="/contact" component={Contact} />*/}
        </Switch>
    </div>
  </Router>
);
ReactDOM.render(routing, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
