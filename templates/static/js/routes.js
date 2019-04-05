import React from 'react';
import { HashRouter, Route, hashHistory } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';

// import more components
export default (
    <HashRouter history={hashHistory}>
     <div>
      <Route path='/' component={Home} />
     </div>
     <div>
       <Route path = '/' component={Map} />
     </div>
     <div>
       <Route path = '/' component={ResultsContainer} />
     </div>
    </HashRouter>
);
