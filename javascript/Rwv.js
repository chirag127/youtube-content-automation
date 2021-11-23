// ==UserScript==
// @name         Remove watched videos
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Remove watched videos from the watchlater list as soon as the http://www.youtube.com/playlist?list=WL is loaded
// @author       Chirag Singhal
// @match        https://www.youtube.com/playlist?list=WL
// @icon         https://www.google.com/s2/favicons?domain=youtube.com
// @grant        none
// ==/UserScript==

(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("button[aria-label='Action menu']")[0].click();
    document
      .querySelector(
        "#items > ytd-menu-service-item-renderer:nth-child(2) > tp-yt-paper-item"
      )
      .click();

    // window.onload = document.querySelector("#items > ytd-menu-service-item-renderer.style-scope.ytd-menu-popup-renderer.iron-selected[aria-selected='false']").click();
    // document.querySelector("#items > ytd-menu-service-item-renderer.style-scope.ytd-menu-popup-renderer:last-child > tp-yt-paper-item.style-scope.ytd-menu-service-item-renderer > yt-formatted-string.style-scope.ytd-menu-service-item-renderer:last-child#items > ytd-menu-service-item-renderer:nth-child(2) > tp-yt-paper-item").click();
    // var removewatched = document.querySelector("#items > ytd-menu-service-item-renderer:nth-child(2) > tp-yt-paper-item");
    // removewatched.click();
    // var removewatchedbutton = document.querySelector("#button").click();
    // removewatchedbutton.click();
    // var removewatch = document.querySelector("#items > ytd-menu-service-item-renderer:nth-child(2) > tp-yt-paper-item")//document.querySelector("#items > ytd-menu-service-item-renderer:nth-child(2) > tp-yt-paper-item > yt-formatted-string");
    // removewatch.click();
  });
})();
