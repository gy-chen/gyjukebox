(this["webpackJsonpgyjukebox-web"]=this["webpackJsonpgyjukebox-web"]||[]).push([[0],[,,,function(e,t,n){e.exports={headerRowContainer:"SearchList_headerRowContainer__27NaD",rowContainer:"SearchList_rowContainer__1Ed_j",rowHeader:"SearchList_rowHeader__2B7vq",albumRowContainer:"SearchList_albumRowContainer__lkJqm",artistRowContainer:"SearchList_artistRowContainer__16kJT",trackRowContainer:"SearchList_trackRowContainer__yQ_-R",playlistRowContainer:"SearchList_playlistRowContainer__3KWy0",removeDefaultListItemStyle:"SearchList_removeDefaultListItemStyle__1G_fk",removeDefaultListStyle:"SearchList_removeDefaultListStyle__2aqII"}},,,,,,,,,,,function(e,t,n){e.exports={container:"Login_container__27oOZ",loginButton:"Login_loginButton__3JQWQ",googleLoginButton:"Login_googleLoginButton__1P3JC",spotifyLoginButton:"Login_spotifyLoginButton__1HTjs"}},,function(e,t,n){e.exports={container:"SearchBar_container__mRTEy",searchInput:"SearchBar_searchInput__15KuH",searchButton:"SearchBar_searchButton__1x_vH",searchIcon:"SearchBar_searchIcon__22R76"}},function(e,t,n){e.exports={container:"Tabs_container__3sqD1",item:"Tabs_item__mgt_V",active:"Tabs_active__307tB"}},function(e,t,n){e.exports={container:"CurrentTrack_container__2tP24",titleContainer:"CurrentTrack_titleContainer__1OyeW",trackName:"CurrentTrack_trackName__2-W8x",userContainer:"CurrentTrack_userContainer__3l_it"}},function(e,t,n){e.exports={container:"App_container__3iLfG",headerBarContainer:"App_headerBarContainer__1EjGg",bodyContainer:"App_bodyContainer__3A_kC",footerBarContainer:"App_footerBarContainer__neaEC"}},,function(e,t,n){e.exports={container:"AlbumListItem_container__22gww",queueButton:"AlbumListItem_queueButton__2bWGH ListItem_operationIcon__3SGuX",queuedButton:"AlbumListItem_queuedButton__1yXsE ListItem_operationIcon__3SGuX"}},function(e,t,n){e.exports={container:"PlaylistListItem_container__1E4I8",queueButton:"PlaylistListItem_queueButton__2KYjp ListItem_operationIcon__3SGuX",queuedButton:"PlaylistListItem_queuedButton__17OaI ListItem_operationIcon__3SGuX"}},function(e,t,n){e.exports={container:"TrackListItem_container__1REr3",queueButton:"TrackListItem_queueButton__2XZ7W ListItem_operationIcon__3SGuX",queuedButton:"TrackListItem_queuedButton__2L4Uh ListItem_operationIcon__3SGuX"}},,function(e,t,n){e.exports={container:"LogoutButton_container__1sDNm",exitIcon:"LogoutButton_exitIcon__XVdjf"}},function(e,t,n){e.exports={container:"Spinner_container__3Hql7",spinner:"Spinner_spinner__j0DNy",spin:"Spinner_spin__1jK-3"}},,,,,,,,,,,,,function(e,t,n){e.exports={container:"HeaderBar_container__3RWLn"}},,,function(e,t,n){e.exports={container:"PlayButton_container__2wtmu"}},function(e,t,n){e.exports={container:"FooterBar_container__1yaA6"}},function(e,t,n){e.exports={item:"AlbumColumnItem_item__HfS3o ColumnItem_item__hfWEn"}},function(e,t,n){e.exports={item:"ArtistColumnItem_item__3PZ5Y ColumnItem_item__hfWEn"}},function(e,t,n){e.exports={seperator:"ArtistsColumnItem_seperator__2zIqz"}},function(e,t,n){e.exports={container:"ArtistListItem_container__2T-wv"}},function(e,t,n){e.exports={item:"PlaylistColumnItem_item__3pIYf ColumnItem_item__hfWEn"}},,function(e,t,n){e.exports={container:"Lyrics_container__XgMe2"}},,function(e,t,n){e.exports=n(78)},,,,,function(e,t,n){},,,,,,,,,,,,,,,,,,,,,function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),i=n(36),o=n.n(i),c=(n(57),n(10)),s=n(24),u=n(1),l=n.n(u),_=n(5),m=n(6),h=n(8),p=n(7),d=n(2),k=n(9),f=n(14),b=n.n(f),v=function(e){function t(e){var n;return Object(_.a)(this,t),(n=Object(h.a)(this,Object(p.a)(t).call(this,e)))._onLoginGoogleButtonClick=n._onLoginGoogleButtonClick.bind(Object(d.a)(n)),n._onLoginSpotifyButtonClick=n._onLoginSpotifyButtonClick.bind(Object(d.a)(n)),n}return Object(k.a)(t,e),Object(m.a)(t,[{key:"componentDidMount",value:function(){var e=this.props.onLoginCallback,t=new URLSearchParams(window.location.search).get("token")||localStorage.getItem("LoginToken");t&&(localStorage.setItem("LoginToken",t),e&&e(t))}},{key:"_onLoginGoogleButtonClick",value:function(){window.open("https://jukebox.gyhost.icu/login/google?callback_url=https://jukebox.gyhost.icu","_self")}},{key:"_onLoginSpotifyButtonClick",value:function(){window.open("https://jukebox.gyhost.icu/login/spotify?callback_url=https://jukebox.gyhost.icu","_self")}},{key:"render",value:function(){return r.a.createElement("div",{className:b.a.container},r.a.createElement("h1",null,"GYJUKEBOX"),r.a.createElement("button",{onClick:this._onLoginGoogleButtonClick,className:"".concat(b.a.loginButton," ").concat(b.a.googleLoginButton)},"Login with Google"),r.a.createElement("button",{onClick:this._onLoginSpotifyButtonClick,className:"".concat(b.a.loginButton," ").concat(b.a.spotifyLoginButton)},"Login with Spotify"))}}]),t}(r.a.Component),C=n(51),y=n(37),E=n(16),A=n.n(E),S=function(e){var t=e.onSearchButtonClick,n=r.a.useState(""),a=Object(C.a)(n,2),i=a[0],o=a[1],c=function(e){e.preventDefault(),t&&t(i)};return r.a.createElement("form",{className:A.a.container,onSubmit:c},r.a.createElement("input",{type:"text",className:A.a.searchInput,value:i,onChange:function(e){return o(e.target.value)}}),r.a.createElement("button",{className:A.a.searchButton,onClick:c},r.a.createElement(y.a,{className:A.a.searchIcon})))},w=n(17),B=n.n(w),g={HOME:1,MY_PLAYLISTS:2,MY_ALBUMS:3,MY_ARTISTS:4,MY_TRACKS:5,LYRICS:6,SEARCH:7},L=function(e){var t=e.activeTab,n=function(e){return e===t?"".concat(B.a.item," ").concat(B.a.active):B.a.item},a=function(t){var n=e.onTabChangeButtonClick;n&&n(t)};return r.a.createElement("div",{className:B.a.container},r.a.createElement("div",{className:n(g.HOME),onClick:function(){return a(g.HOME)}},"HOME"),r.a.createElement("div",{className:n(g.MY_PLAYLISTS),onClick:function(){return a(g.MY_PLAYLISTS)}},"MY PLAYLISTS"),r.a.createElement("div",{className:n(g.MY_ALBUMS),onClick:function(){return a(g.MY_ALBUMS)}},"MY ALBUMS"),r.a.createElement("div",{className:n(g.MY_ARTISTS),onClick:function(){return a(g.MY_ARTISTS)}},"MY ARTISTS"),r.a.createElement("div",{className:n(g.MY_TRACKS),onClick:function(){return a(g.MY_TRACKS)}},"MY TRACKS"),r.a.createElement("div",{className:n(g.LYRICS),onClick:function(){return a(g.LYRICS)}},"LYRICS"),t===g.SEARCH?r.a.createElement("div",{className:n(g.SEARCH),onClick:function(){return a(g.SEARCH)}},"SERACH"):null)},T=n(38),I=n(25),x=n.n(I),P=function(e){return r.a.createElement("div",{className:x.a.container,onClick:function(){var t=e.onLogoutButtonClick;t&&t()}},r.a.createElement(T.a,{className:x.a.exitIcon}))},O=n(39),j=n.n(O),R=function(e){var t=e.activeTab,n=e.onSearchButtonClick,a=e.onTabChangeButtonClick,i=e.onLogoutButtonClick;return r.a.createElement("div",{className:j.a.container},r.a.createElement(S,{onSearchButtonClick:n}),r.a.createElement(L,{activeTab:t,onTabChangeButtonClick:a}),r.a.createElement(P,{onLogoutButtonClick:i}))},N=n(20),Q=n(3),H=n.n(Q),D=function(e){function t(e){var n;return Object(_.a)(this,t),(n=Object(h.a)(this,Object(p.a)(t).call(this,e)))._renderAlbums=n._renderAlbums.bind(Object(d.a)(n)),n._renderArtists=n._renderArtists.bind(Object(d.a)(n)),n._renderPlaylists=n._renderPlaylists.bind(Object(d.a)(n)),n._renderTracks=n._renderTracks.bind(Object(d.a)(n)),n._isTrackInQueue=n._isTrackInQueue.bind(Object(d.a)(n)),n._isAlbumInQueue=n._isAlbumInQueue.bind(Object(d.a)(n)),n._isPlaylistInQueue=n._isPlaylistInQueue.bind(Object(d.a)(n)),n}return Object(k.a)(t,e),Object(m.a)(t,[{key:"_renderAlbums",value:function(){var e=this,t=this.props,n=t.albums,a=t.albumComponent,i=t.onViewAlbumButtonClick,o=t.onViewArtistButtonClick,c=t.onQueueAlbumButtonClick;return a&&n&&0!==n.length?r.a.createElement(r.a.Fragment,null,r.a.createElement("li",{className:"".concat(H.a.albumRowContainer," ").concat(H.a.headerRowContainer)},r.a.createElement("div",{className:H.a.rowHeader},"Album"),r.a.createElement("div",{className:H.a.rowHeader},"Artist"),r.a.createElement("div",{className:H.a.rowHeader},r.a.createElement(N.a,null))),n.map((function(t){return r.a.createElement("li",{className:"".concat(H.a.removeDefaultListItemStyle," ").concat(H.a.rowContainer)},r.a.createElement(a,{album:t,onViewAlbumButtonClick:i,onViewArtistButtonClick:o,onQueueAlbumButtonClick:c,inQueue:e._isAlbumInQueue(t)}))}))):null}},{key:"_renderArtists",value:function(){var e=this.props,t=e.artists,n=e.artistComponent,a=e.onViewArtistButtonClick;return n&&t&&0!==t.length?r.a.createElement(r.a.Fragment,null,r.a.createElement("li",{key:"artistsHeaderRow",className:"".concat(H.a.headerRowContainer," ").concat(H.a.artistRowContainer)},r.a.createElement("div",{className:H.a.rowHeader},"Artist")),t.map((function(e){return r.a.createElement("li",{key:e.uri,className:"".concat(H.a.removeDefaultListItemStyle," ").concat(H.a.rowContainer)},r.a.createElement(n,{artist:e,onViewArtistButtonClick:a}))}))):null}},{key:"_renderPlaylists",value:function(){var e=this,t=this.props,n=t.playlists,a=t.playlistComponent,i=t.onViewPlaylistButtonClick,o=t.onQueuePlaylistButtonClick;return a&&n&&0!==n.length?r.a.createElement(r.a.Fragment,null,r.a.createElement("li",{key:"playlistsHeaderRow",className:"".concat(H.a.headerRowContainer," ").concat(H.a.playlistRowContainer)},r.a.createElement("div",{className:H.a.rowHeader},"Playlist"),r.a.createElement("div",{className:H.a.rowHeader},"Owner"),r.a.createElement("div",{className:H.a.rowHeader},r.a.createElement(N.a,null))),n.map((function(t){return r.a.createElement("li",{key:t.uri,className:"".concat(H.a.removeDefaultListItemStyle," ").concat(H.a.rowContainer)},r.a.createElement(a,{playlist:t,onViewPlaylistButtonClick:i,onQueuePlaylistButtonClick:o,inQueue:e._isPlaylistInQueue(t)}))}))):null}},{key:"_isTrackInQueue",value:function(e){return this.props.inQueueTracks.map((function(e){return e.uri})).includes(e.uri)}},{key:"_isAlbumInQueue",value:function(e){return this.props.inQueueAlbums.map((function(e){return e.uri})).includes(e.uri)}},{key:"_isPlaylistInQueue",value:function(e){return this.props.inQueuePlaylists.map((function(e){return e.uri})).includes(e.uri)}},{key:"_renderTracks",value:function(){var e=this,t=this.props,n=t.tracks,a=t.trackComponent,i=t.onQueueTrackButtonClick,o=t.onViewAlbumButtonClick,c=t.onViewArtistButtonClick;return a&&n&&0!==n.length?r.a.createElement(r.a.Fragment,null,r.a.createElement("li",{key:"tracksHeaderRow",className:"".concat(H.a.trackRowContainer," ").concat(H.a.headerRowContainer)},r.a.createElement("div",{className:H.a.rowHeader},"Track"),r.a.createElement("div",{className:H.a.rowHeader},"Artist"),r.a.createElement("div",{className:H.a.rowHeader},"Album"),r.a.createElement("div",{className:H.a.rowHeader},r.a.createElement(N.a,null))),n.map((function(t){return r.a.createElement("li",{key:t.uri,className:"".concat(H.a.removeDefaultListItemStyle," ").concat(H.a.rowContainer)},r.a.createElement(a,{track:t,inQueue:e._isTrackInQueue(t),onQueueTrackButtonClick:i,onViewAlbumButtonClick:o,onViewArtistButtonClick:c}))}))):null}},{key:"render",value:function(){return r.a.createElement(r.a.Fragment,null,r.a.createElement("ul",{className:H.a.removeDefaultListStyle},this._renderAlbums()),r.a.createElement("ul",{className:H.a.removeDefaultListStyle},this._renderArtists()),r.a.createElement("ul",{className:H.a.removeDefaultListStyle},this._renderPlaylists()),r.a.createElement("ul",{className:H.a.removeDefaultListStyle},this._renderTracks()))}}]),t}(r.a.Component);D.defaultProps={inQueueTracks:[],inQueueAlbums:[],inQueuePlaylists:[]};var M=D,Y=n(40),V=n(41),U=n(18),q=n.n(U),G=function(e){var t=e.track,n=e.user;return t?r.a.createElement("div",{className:q.a.container},r.a.createElement("div",{className:q.a.titleContainer},r.a.createElement("span",{className:q.a.trackName},t.name),r.a.createElement(Y.a,null),r.a.createElement("span",null,t.artists.map((function(e){return e.name})).join(", "))),r.a.createElement("div",{className:q.a.userContainer},r.a.createElement(V.a,null),r.a.createElement("span",null,n.name))):null},W=n(42),X=n.n(W),K=function(e){var t=e.onPlayButtonClick;return r.a.createElement("div",{className:X.a.container,onClick:t},"Play")},F=n(43),J=n.n(F),z=function(e){var t=e.displayPlayButton,n=e.currentTrack;n=n||{};var a=function(){var t=e.onPlayButtonClick;t&&t()};return r.a.createElement("div",{className:J.a.container},r.a.createElement(G,{user:n.user,track:n.track}),t&&n.track?r.a.createElement(K,{onPlayButtonClick:a}):null)},Z=n(44),$=n.n(Z),ee=function(e){var t=e.album;return r.a.createElement("div",null,r.a.createElement("span",{className:$.a.item,onClick:function(){var n=e.onViewAlbumButtonClick;n&&n(t)}},t.name))},te=n(45),ne=n.n(te),ae=function(e){var t=e.artist;return r.a.createElement("span",{className:ne.a.item,onClick:function(){var n=e.onViewArtistButtonClick;n&&n(t)}},t.name)},re=n(46),ie=n.n(re),oe=function(e){var t=e.artists;return function(){var n=e.onViewArtistButtonClick;return t.reduce((function(e,a,i){return e.push(r.a.createElement(ae,{artist:a,onViewArtistButtonClick:n})),i!==t.length-1&&e.push(r.a.createElement("span",{className:ie.a.seperator},", ")),e}),[])}()},ce=n(11),se=n(12),ue=n(21),le=n.n(ue),_e=function(e){var t=e.album,n=e.onViewAlbumButtonClick,a=e.onViewArtistButtonClick,i=function(){var n=e.onQueueAlbumButtonClick;n&&n(t)};return r.a.createElement("div",{className:le.a.container},r.a.createElement("div",null,r.a.createElement(ee,{album:t,onViewAlbumButtonClick:n})),r.a.createElement("div",null,r.a.createElement(oe,{artists:t.artists,onViewArtistButtonClick:a})),r.a.createElement("div",null,e.inQueue?r.a.createElement(se.a,{className:le.a.queuedButton}):r.a.createElement(ce.a,{onClick:i,className:le.a.queueButton})))},me=n(47),he=n.n(me),pe=function(e){var t=e.artist,n=e.onViewArtistButtonClick;return r.a.createElement("div",{className:he.a.container},r.a.createElement("div",null,r.a.createElement(ae,{artist:t,onViewArtistButtonClick:n})))},de=n(48),ke=n.n(de),fe=function(e){var t=e.playlist;return r.a.createElement("span",{className:ke.a.item,onClick:function(){var n=e.onViewPlaylistButtonClick;n&&n(t)}},t.name)},be=n(22),ve=n.n(be),Ce=function(e){var t=e.playlist,n=e.onViewPlaylistButtonClick,a=function(){var n=e.onQueuePlaylistButtonClick;n&&n(t)};return r.a.createElement("div",{className:ve.a.container},r.a.createElement("div",null,r.a.createElement(fe,{playlist:t,onViewPlaylistButtonClick:n})),r.a.createElement("div",null,t.owner.display_name),r.a.createElement("div",null,e.inQueue?r.a.createElement(se.a,{className:ve.a.queuedButton}):r.a.createElement(ce.a,{onClick:a,className:ve.a.queueButton})))},ye=n(23),Ee=n.n(ye),Ae=function(e){var t=e.track,n=e.onViewArtistButtonClick,a=function(){var n=e.onQueueTrackButtonClick;n&&n(t)};return r.a.createElement("div",{className:Ee.a.container},r.a.createElement("div",null,t.name),r.a.createElement("div",null,r.a.createElement(oe,{artists:t.artists,onViewArtistButtonClick:n})),r.a.createElement("div",null,r.a.createElement(ee,{album:t.album,onViewAlbumButtonClick:function(){var n=e.onViewAlbumButtonClick;n&&n(t.album)}})),r.a.createElement("div",null,e.inQueue?r.a.createElement(se.a,{className:Ee.a.queuedButton}):r.a.createElement(ce.a,{onClick:a,className:Ee.a.queueButton})))},Se=n(13),we=n.n(Se),Be=n(49),ge=n.n(Be).a.create({baseURL:"https://jukebox.gyhost.icu"}),Le=function(e){var t,n,a=arguments;return l.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return t=a.length>1&&void 0!==a[1]?a[1]:0,r.next=3,l.a.awrap(ge.get("/search",{params:{q:e,offset:t}}));case 3:return n=r.sent,r.abrupt("return",n.data);case 5:case"end":return r.stop()}}))},Te=function(e){return ge.post("/track/".concat(e.id,"/enqueue"))},Ie=function(e){return ge.post("/album/".concat(e.id,"/enqueue"))},xe=function(e){return ge.post("/playlist/".concat(e.id,"/enqueue"))},Pe=function(){var e,t;return l.a.async((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,l.a.awrap(ge.get("/track/current"));case 2:if(e=n.sent,t=e.data){n.next=6;break}return n.abrupt("return",{track:null,user:null});case 6:return n.abrupt("return",t);case 7:case"end":return n.stop()}}))},Oe=function(){var e;return l.a.async((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,l.a.awrap(ge.get("/lyrics/current"));case 2:return e=t.sent,t.abrupt("return",e.data);case 4:case"end":return t.stop()}}))},je=function(e){var t,n,a,r=arguments;return l.a.async((function(i){for(;;)switch(i.prev=i.next){case 0:return t=r.length>1&&void 0!==r[1]?r[1]:0,n={offset:t},i.next=4,l.a.awrap(ge.get("/album/".concat(e.id,"/tracks"),{params:n}));case 4:return(a=i.sent).data.tracks.forEach((function(t){return t.album=e})),i.abrupt("return",a.data);case 7:case"end":return i.stop()}}))},Re=function(e){var t,n,a,r=arguments;return l.a.async((function(i){for(;;)switch(i.prev=i.next){case 0:return t=r.length>1&&void 0!==r[1]?r[1]:0,n={offset:t},i.next=4,l.a.awrap(ge.get("/artist/".concat(e.id,"/details"),{params:n}));case 4:return a=i.sent,i.abrupt("return",a.data);case 6:case"end":return i.stop()}}))},Ne=function(e){var t,n,a,r=arguments;return l.a.async((function(i){for(;;)switch(i.prev=i.next){case 0:return t=r.length>1&&void 0!==r[1]?r[1]:0,n={offset:t},i.next=4,l.a.awrap(ge.get("/playlist/".concat(e.id,"/tracks"),{params:n}));case 4:return(a=i.sent).data.tracks=a.data.tracks.map((function(e){return e.track})),i.abrupt("return",a.data);case 7:case"end":return i.stop()}}))},Qe=function(){var e,t,n,a=arguments;return l.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return e=a.length>0&&void 0!==a[0]?a[0]:0,t={offset:e},r.next=4,l.a.awrap(ge.get("/me/top",{params:t}));case 4:return n=r.sent,r.abrupt("return",n.data);case 6:case"end":return r.stop()}}))},He=function(){var e,t,n,a=arguments;return l.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return e=a.length>0&&void 0!==a[0]?a[0]:0,t={offset:e},r.next=4,l.a.awrap(ge.get("/me/playlists",{params:t}));case 4:return n=r.sent,r.abrupt("return",n.data);case 6:case"end":return r.stop()}}))},De=function(){var e,t,n,a=arguments;return l.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return e=a.length>0&&void 0!==a[0]?a[0]:0,t={offset:e},r.next=4,l.a.awrap(ge.get("/me/albums",{params:t}));case 4:return(n=r.sent).data.albums=n.data.albums.map((function(e){return e.album})),r.abrupt("return",n.data);case 7:case"end":return r.stop()}}))},Me=function(){var e,t,n,a=arguments;return l.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return e=a.length>0&&void 0!==a[0]?a[0]:null,t={after:e},r.next=4,l.a.awrap(ge.get("/me/artists",{params:t}));case 4:return n=r.sent,r.abrupt("return",n.data);case 6:case"end":return r.stop()}}))},Ye=function(){var e,t,n,a=arguments;return l.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return e=a.length>0&&void 0!==a[0]?a[0]:0,t={offset:e},r.next=4,l.a.awrap(ge.get("/me/tracks",{params:t}));case 4:return(n=r.sent).data.tracks=n.data.tracks.map((function(e){return e.track})),r.abrupt("return",n.data);case 7:case"end":return r.stop()}}))},Ve=function(e){function t(e){var n;return Object(_.a)(this,t),(n=Object(h.a)(this,Object(p.a)(t).call(this,e)))._poll=n._poll.bind(Object(d.a)(n)),n._pollingInterval=null,n._previousCurrentTrack=null,n}return Object(k.a)(t,e),Object(m.a)(t,[{key:"componentDidMount",value:function(){this._pollingInterval=setInterval(this._poll,2e3)}},{key:"componentWillUnmount",value:function(){clearInterval(this._pollingInterval),this._pollingInterval=null}},{key:"_poll",value:function(){var e,t;return l.a.async((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,l.a.awrap(Pe());case 2:e=n.sent,we.a.isEqual(this._previousCurrentTrack,e)||((t=this.props.onCurrentTrackChange)&&t(e),this._previousCurrentTrack=e);case 4:case"end":return n.stop()}}),null,this)}},{key:"render",value:function(){return null}}]),t}(r.a.Component),Ue=n(15),qe=n.n(Ue),Ge="https://jukebox.gyhost.icu/hls/playlist.m3u8",We=function(e){function t(e){var n;return Object(_.a)(this,t),(n=Object(h.a)(this,Object(p.a)(t).call(this,e)))._onMediaAttached=n._onMediaAttached.bind(Object(d.a)(n)),n._onManifestParsed=n._onManifestParsed.bind(Object(d.a)(n)),n._onError=n._onError.bind(Object(d.a)(n)),n._retryLoadResource=we.a.throttle(n._retryLoadResource.bind(Object(d.a)(n)),2e3),n._audioRef=r.a.createRef(),n._hls=null,n._mediaParsed=!1,n}return Object(k.a)(t,e),Object(m.a)(t,[{key:"componentDidMount",value:function(){qe.a.isSupported()?(this._hls=new qe.a,this._hls.attachMedia(this._audioRef.current),this._hls.on(qe.a.Events.MEDIA_ATTACHED,this._onMediaAttached)):(this._audioRef.current.src=Ge,this._audioRef.current.addEventListener("loadedmetadata",this._onManifestParsed))}},{key:"componentDidUpdate",value:function(e){var t=e.prevPlay,n=this.props;t!==n&&(n?this._audioRef.current.play():this._audioRef.current.pause())}},{key:"componentWillUnmount",value:function(){this._hls&&this._hls.destroy()}},{key:"_onMediaAttached",value:function(){this._hls.loadSource(Ge),this._hls.on(qe.a.Events.MANIFEST_PARSED,this._onManifestParsed),this._hls.on(qe.a.Events.ERROR,this._onError)}},{key:"_onManifestParsed",value:function(){var e=this.props.onPlayerReady;this._mediaParsed=!0,e&&e()}},{key:"_onError",value:function(e,t){t.fatal&&(console.log("encounter fatal error, try to recover",t),this._mediaParsed?this._hls.startLoad():this._retryLoadResource())}},{key:"_retryLoadResource",value:function(){this._hls.loadSource(Ge)}},{key:"render",value:function(){return r.a.createElement("audio",{ref:this._audioRef})}}]),t}(r.a.PureComponent),Xe=n(26),Ke=n.n(Xe),Fe=function(){return r.a.createElement("div",{className:Ke.a.container},r.a.createElement("span",{className:Ke.a.spinner}))},Je=n(19),ze=n.n(Je),Ze=n(50),$e=n.n(Ze),et=function(e){var t=e.title,n=e.artist,a=e.lyrics;return we.a.isEmpty(a)?null:r.a.createElement("div",{className:$e.a.container},r.a.createElement("h3",null,"".concat(t," - ").concat(n)),r.a.createElement("pre",null,a))},tt={WAIT:1,READY:2,PLAY:3},nt={LOADING:1,DONE:2},at=function(e){function t(e){var n;return Object(_.a)(this,t),(n=Object(h.a)(this,Object(p.a)(t).call(this,e)))._EMPTY_SEARCH_LIST_DATA={albums:null,artists:null,playlists:null,tracks:null},n._INITIAL_STATE={login:{isLogin:!1,token:null},inQueueTracks:[],inQueueAlbums:[],inQueuePlaylists:[],currentTrack:null,currentSearchListData:n._EMPTY_SEARCH_LIST_DATA,playerState:tt.WAIT,currentLyrics:null,loadingState:nt.DONE,tab:g.HOME},n._wrapLoadingAction=n._wrapLoadingAction.bind(Object(d.a)(n)),n._onPlayButtonClick=n._onPlayButtonClick.bind(Object(d.a)(n)),n._onPlayerReady=n._onPlayerReady.bind(Object(d.a)(n)),n._onPopState=n._onPopState.bind(Object(d.a)(n)),n._pushState=n._pushState.bind(Object(d.a)(n)),n._onCurrentTrackChange=n._onCurrentTrackChange.bind(Object(d.a)(n)),n._onLoginCallback=n._onLoginCallback.bind(Object(d.a)(n)),n._onQueueTrackButtonClick=n._onQueueTrackButtonClick.bind(Object(d.a)(n)),n._onQueueAlbumButtonClick=n._onQueueAlbumButtonClick.bind(Object(d.a)(n)),n._onQueuePlaylistButtonClick=n._onQueuePlaylistButtonClick.bind(Object(d.a)(n)),n._onViewAlbumButtonClick=n._wrapLoadingAction(n._onViewAlbumButtonClick.bind(Object(d.a)(n))),n._onViewArtistButtonClick=n._wrapLoadingAction(n._onViewArtistButtonClick.bind(Object(d.a)(n))),n._onViewPlaylistButtonClick=n._wrapLoadingAction(n._onViewPlaylistButtonClick.bind(Object(d.a)(n))),n._onSearchButtonClick=n._wrapLoadingAction(n._onSearchButtonClick.bind(Object(d.a)(n))),n._refreshTabContent=n._refreshTabContent.bind(Object(d.a)(n)),n._refreshUserTop=n._wrapLoadingAction(n._refreshUserTop.bind(Object(d.a)(n))),n._refreshUserPlaylists=n._wrapLoadingAction(n._refreshUserPlaylists.bind(Object(d.a)(n))),n._refreshUserAlbums=n._wrapLoadingAction(n._refreshUserAlbums.bind(Object(d.a)(n))),n._refreshUserArtists=n._wrapLoadingAction(n._refreshUserArtists.bind(Object(d.a)(n))),n._refreshUserTracks=n._wrapLoadingAction(n._refreshUserTracks.bind(Object(d.a)(n))),n._onTabChangeButtonClick=n._onTabChangeButtonClick.bind(Object(d.a)(n)),n._onLogoutButtonClick=n._onLogoutButtonClick.bind(Object(d.a)(n)),n._logout=n._logout.bind(Object(d.a)(n)),n._commonApiErrorHandle=n._commonApiErrorHandle.bind(Object(d.a)(n)),n._updateCurrentLyrics=n._updateCurrentLyrics.bind(Object(d.a)(n)),n._renderBody=n._renderBody.bind(Object(d.a)(n)),n.state=n._INITIAL_STATE,window.onpopstate=n._onPopState,n}return Object(k.a)(t,e),Object(m.a)(t,[{key:"componentDidUpdate",value:function(e,t){t.tab!==this.state.tab&&this._refreshTabContent()}},{key:"_wrapLoadingAction",value:function(e){var t=this;return function(){var n=arguments;return l.a.async((function(a){for(;;)switch(a.prev=a.next){case 0:return t.setState({loadingState:nt.LOADING}),a.prev=1,a.next=4,l.a.awrap(e.apply(void 0,n));case 4:return a.prev=4,t.setState({loadingState:nt.DONE}),a.finish(4);case 7:case"end":return a.stop()}}),null,null,[[1,,4,7]])}}},{key:"_onPlayButtonClick",value:function(){this.state.playerState===tt.READY&&this.setState({playerState:tt.PLAY})}},{key:"_onPlayerReady",value:function(){this.state.playerState===tt.WAIT&&this.setState({playerState:tt.READY})}},{key:"_onPopState",value:function(e){"logged_out"===e.state?window.history.pushState("logged_out",null,"/"):this.setState(e.state)}},{key:"_pushState",value:function(){var e=this.state,t=e.currentSearchListData,n=e.tab;window.history.pushState({currentSearchListData:t,tab:n},null,"/")}},{key:"_onCurrentTrackChange",value:function(e){this.setState({currentTrack:e}),this._updateCurrentLyrics()}},{key:"_onLoginCallback",value:function(e){var t=this;this.setState({login:{isLogin:!0,token:e}},(function(){!function(e){ge.defaults.headers.common.Authorization="Bearer ".concat(e)}(e),window.history.replaceState(t._EMPTY_SEARCH_LIST_DATA,null,"/"),t._refreshTabContent()}))}},{key:"_onQueueTrackButtonClick",value:function(e){return l.a.async((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,l.a.awrap(Te(e));case 3:this.setState((function(t){return{inQueueTracks:[].concat(Object(s.a)(t.inQueueTracks),[e])}})),t.next=9;break;case 6:t.prev=6,t.t0=t.catch(0),this._commonApiErrorHandle(t.t0);case 9:case"end":return t.stop()}}),null,this,[[0,6]])}},{key:"_onQueueAlbumButtonClick",value:function(e){return l.a.async((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,l.a.awrap(Ie(e));case 3:this.setState((function(t){return{inQueueAlbums:[].concat(Object(s.a)(t.inQueueAlbums),[e])}})),t.next=9;break;case 6:t.prev=6,t.t0=t.catch(0),this._commonApiErrorHandle(t.t0);case 9:case"end":return t.stop()}}),null,this,[[0,6]])}},{key:"_onQueuePlaylistButtonClick",value:function(e){return l.a.async((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,l.a.awrap(xe(e));case 3:this.setState((function(t){return{inQueuePlaylists:[].concat(Object(s.a)(t.inQueuePlaylists),[e])}})),t.next=9;break;case 6:t.prev=6,t.t0=t.catch(0),this._commonApiErrorHandle(t.t0);case 9:case"end":return t.stop()}}),null,this,[[0,6]])}},{key:"_onViewAlbumButtonClick",value:function(e){var t,n;return l.a.async((function(a){for(;;)switch(a.prev=a.next){case 0:return a.prev=0,a.next=3,l.a.awrap(je(e));case 3:t=a.sent,n=t.tracks,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{tracks:n})},this._pushState),a.next=11;break;case 8:a.prev=8,a.t0=a.catch(0),this._commonApiErrorHandle(a.t0);case 11:case"end":return a.stop()}}),null,this,[[0,8]])}},{key:"_onViewArtistButtonClick",value:function(e){var t,n,a;return l.a.async((function(r){for(;;)switch(r.prev=r.next){case 0:return r.prev=0,r.next=3,l.a.awrap(Re(e));case 3:t=r.sent,n=t.tracks,a=t.albums,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{tracks:n,albums:a})},this._pushState),r.next=12;break;case 9:r.prev=9,r.t0=r.catch(0),this._commonApiErrorHandle(r.t0);case 12:case"end":return r.stop()}}),null,this,[[0,9]])}},{key:"_onViewPlaylistButtonClick",value:function(e){var t,n;return l.a.async((function(a){for(;;)switch(a.prev=a.next){case 0:return a.prev=0,a.next=3,l.a.awrap(Ne(e));case 3:t=a.sent,n=t.tracks,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{tracks:n})},this._pushState),a.next=11;break;case 8:a.prev=8,a.t0=a.catch(0),this._commonApiErrorHandle(a.t0);case 11:case"end":return a.stop()}}),null,this,[[0,8]])}},{key:"_onSearchButtonClick",value:function(e){var t,n,a,r,i;return l.a.async((function(o){for(;;)switch(o.prev=o.next){case 0:return o.prev=0,o.next=3,l.a.awrap(Le(e));case 3:t=o.sent,n=t.albums,a=t.artists,r=t.tracks,i=t.playlists,this.setState({tab:g.SEARCH,currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{albums:n,artists:a,playlists:i,tracks:r})},this._pushState),o.next=14;break;case 11:o.prev=11,o.t0=o.catch(0),this._commonApiErrorHandle(o.t0);case 14:case"end":return o.stop()}}),null,this,[[0,11]])}},{key:"_updateCurrentLyrics",value:function(){var e;return l.a.async((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,l.a.awrap(Oe());case 2:e=t.sent,this.setState({currentLyrics:e});case 4:case"end":return t.stop()}}),null,this)}},{key:"_refreshTabContent",value:function(){switch(this.state.tab){case g.HOME:this._refreshUserTop();break;case g.MY_PLAYLISTS:this._refreshUserPlaylists();break;case g.MY_ALBUMS:this._refreshUserAlbums();break;case g.MY_ARTISTS:this._refreshUserArtists();break;case g.MY_TRACKS:this._refreshUserTracks()}}},{key:"_refreshUserTop",value:function(){var e,t,n;return l.a.async((function(a){for(;;)switch(a.prev=a.next){case 0:return a.prev=0,a.next=3,l.a.awrap(Qe());case 3:e=a.sent,t=e.artists,n=e.tracks,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{artists:t,tracks:n})},this._pushState),a.next=12;break;case 9:a.prev=9,a.t0=a.catch(0),this._commonApiErrorHandle(a.t0);case 12:case"end":return a.stop()}}),null,this,[[0,9]])}},{key:"_refreshUserPlaylists",value:function(){var e,t;return l.a.async((function(n){for(;;)switch(n.prev=n.next){case 0:return n.prev=0,n.next=3,l.a.awrap(He());case 3:e=n.sent,t=e.playlists,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{playlists:t})},this._pushState),n.next=11;break;case 8:n.prev=8,n.t0=n.catch(0),this._commonApiErrorHandle(n.t0);case 11:case"end":return n.stop()}}),null,this,[[0,8]])}},{key:"_refreshUserAlbums",value:function(){var e,t;return l.a.async((function(n){for(;;)switch(n.prev=n.next){case 0:return n.prev=0,n.next=3,l.a.awrap(De());case 3:e=n.sent,t=e.albums,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{albums:t})},this._pushState),n.next=11;break;case 8:n.prev=8,n.t0=n.catch(0),this._commonApiErrorHandle(n.t0);case 11:case"end":return n.stop()}}),null,this,[[0,8]])}},{key:"_refreshUserArtists",value:function(){var e,t;return l.a.async((function(n){for(;;)switch(n.prev=n.next){case 0:return n.prev=0,n.next=3,l.a.awrap(Me());case 3:e=n.sent,t=e.artists,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{artists:t})},this._pushState),n.next=11;break;case 8:n.prev=8,n.t0=n.catch(0),this._commonApiErrorHandle(n.t0);case 11:case"end":return n.stop()}}),null,this,[[0,8]])}},{key:"_refreshUserTracks",value:function(){var e,t;return l.a.async((function(n){for(;;)switch(n.prev=n.next){case 0:return n.prev=0,n.next=3,l.a.awrap(Ye());case 3:e=n.sent,t=e.tracks,this.setState({currentSearchListData:Object(c.a)({},this._EMPTY_SEARCH_LIST_DATA,{tracks:t})},this._pushState),n.next=11;break;case 8:n.prev=8,n.t0=n.catch(0),this._commonApiErrorHandle(n.t0);case 11:case"end":return n.stop()}}),null,this,[[0,8]])}},{key:"_onTabChangeButtonClick",value:function(e){this.setState({tab:e})}},{key:"_logout",value:function(){localStorage.clear(),this.setState(this._INITIAL_STATE),window.history.pushState("logged_out",null,"/")}},{key:"_onLogoutButtonClick",value:function(){this._logout()}},{key:"_commonApiErrorHandle",value:function(e){this._logout()}},{key:"_renderBody",value:function(){if(this.state.tab===g.LYRICS){var e=this.state.currentLyrics;return e?r.a.createElement(et,e):null}var t=this.state,n=t.inQueueTracks,a=t.inQueueAlbums,i=t.inQueuePlaylists,o=t.currentSearchListData;return t.loadingState===nt.LOADING?r.a.createElement(Fe,null):r.a.createElement(M,Object.assign({},o,{inQueueTracks:n,inQueueAlbums:a,inQueuePlaylists:i,albumComponent:_e,artistComponent:pe,playlistComponent:Ce,trackComponent:Ae,onQueueTrackButtonClick:this._onQueueTrackButtonClick,onQueueAlbumButtonClick:this._onQueueAlbumButtonClick,onQueuePlaylistButtonClick:this._onQueuePlaylistButtonClick,onViewAlbumButtonClick:this._onViewAlbumButtonClick,onViewArtistButtonClick:this._onViewArtistButtonClick,onViewPlaylistButtonClick:this._onViewPlaylistButtonClick}))}},{key:"render",value:function(){if(!this.state.login.isLogin)return r.a.createElement(v,{onLoginCallback:this._onLoginCallback});var e=this.state,t=e.tab,n=e.currentTrack,a=e.playerState;return r.a.createElement("div",{className:ze.a.container},r.a.createElement("div",{className:ze.a.headerBarContainer},r.a.createElement(R,{activeTab:t,onSearchButtonClick:this._onSearchButtonClick,onTabChangeButtonClick:this._onTabChangeButtonClick,onLogoutButtonClick:this._onLogoutButtonClick})),r.a.createElement("div",{className:ze.a.bodyContainer},this._renderBody()),r.a.createElement("div",{className:ze.a.footerBarContainer},r.a.createElement(z,{currentTrack:n,displayPlayButton:a===tt.READY,onPlayButtonClick:this._onPlayButtonClick})),r.a.createElement(Ve,{onCurrentTrackChange:this._onCurrentTrackChange}),r.a.createElement(We,{onPlayerReady:this._onPlayerReady,play:a===tt.PLAY}))}}]),t}(r.a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));o.a.render(r.a.createElement(at,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}],[[52,1,2]]]);
//# sourceMappingURL=main.a16d7f68.chunk.js.map