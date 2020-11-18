import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {ProfileBadgeComponent} from './profiles'
import {FeedComponent, Nash-messageComponent, Nash_messageDetailComponent} from './nash-message'
import * as serviceWorker from './serviceWorker';

const appEl = document.getElementById('root')
if (appEl) {
    ReactDOM.render(<App />, appEl);
}
const e = React.createElement
const nash-messageEl = document.getElementById("nasharus")
if (nash-messageEl) {
    ReactDOM.render(
        e(Nash-messageComponent, nash-messageEl.dataset), nash-messageEl);
}

const nash_messageFeedEl = document.getElementById("nasharus-feed")
if (nash_messageFeedEl) {
    ReactDOM.render(
        e(FeedComponent, nash_messageFeedEl.dataset), nash_messageFeedEl);
}

const nash_messageDetailElements = document.querySelectorAll(".nasharus-detail")

nash_messageDetailElements.forEach(container=> {
    ReactDOM.render(
        e(Nash_messageDetailComponent, container.dataset), 
        container);
})

const userProfileBadgeElements = document.querySelectorAll(".nasharus-profile-badge")

userProfileBadgeElements.forEach(container=> {
    ReactDOM.render(
        e(ProfileBadgeComponent, container.dataset), 
        container);
})
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
