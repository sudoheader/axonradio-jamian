
new Vue({
  el: '#app',
  delimiters: ["[[","]]"],
  data: function data() {
    return {
      radios: 'jazz',
      songs: [],
      vidID: 'rY-FJvRqK0E',
      player
    };
  },
  methods: {
    getSongs: function(){
      axios.get('http://127.0.0.1:5000/song/' + this.radios)
      .then(response => {
        this.songs = response.data;
        console.log(response.data);
      })
      .catch(error => {
        console.log(error)
      });
    }//function
  }//methods
});

// var player;
// window.vidIDjs;
// function onYouTubeIframeAPIReady() {
//   player = new YT.Player('player', {
//     height: '390',
//     width: '640',
//     videoId: 'M7lc1UVf-VE',
//     events: {
//       'onReady': onPlayerReady,
//       'onStateChange': onPlayerStateChange
//     }
//   });
// }
