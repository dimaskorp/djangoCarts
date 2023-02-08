'use strict';

if(navigator.userAgent.indexOf('MSIE') !== -1 || navigator.appVersion.indexOf('Trident/') > -1) {
   window.location.replace('/bad_browser/');
}