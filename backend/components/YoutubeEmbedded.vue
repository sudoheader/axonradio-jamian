<template>
    <div class="youtubeembedded">
        <section>
            <youtube :video-id="videoId" @ready="ready" @playing="playing"></youtube>
        </section>
    </div>
</template>

<script>
    export default {
        name: "youtubeembedded",
        data () {
            return {
                videoId: '8XiqrERZo_8'
            };
        },
        methods: {
            ready(player) {
                this.player = player
            },
            playing(player) {
                // The player is playing a video.
            },
            change() {
                // when you change the value, the player will also change.
                // If you would like to change `playerVars`, please change it before you change `videoId`.
                // If `playerVars.autoplay` is 1, `loadVideoById` will be called.
                // If `playerVars.autoplay` is 0, `cueVideoById` will be called.
                this.videoId = '8XiqrERZo_8'
            },
            stop() {
                this.player.stopVideo()
            },
            pause() {
                this.player.pauseVideo()
            }
        }
    }
</script>

<style scoped>

</style>