<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router'

import SearchVideo from './SearchVideo.vue';
import AgendaPoints from '../components/AgendaPoints.vue';
import VideoChat from "../components/VideoChat.vue"

const route = useRoute()

const isHovering = ref(false)
const lineLeft = ref(0)
const videoUrl = ref(null);
const videoDuration = ref(0);
const speakers = ref([])
const agenda = ref([])
const speakerColors = ref({ "": "bg-transparent" })
const agendaColors = ref({ "": "bg-transparent" })
const transcript = ref("No transcript found")
const speakerNameMapping = ref({})

fetch(`http://127.0.0.1:3012/api/getVideoData?gemeente=${route.params.gemeenteName}&meetingType=${route.params.gemeenteType}&year=${route.params.gemeenteYear}&video=${route.params.videoID}.mp4`)
    .then(response => response.json())
    .then(data => {
        videoDuration.value = Math.round(data.duration)
    })

fetch(`http://127.0.0.1:3012/api/getVideo?gemeente=${route.params.gemeenteName}&meetingType=${route.params.gemeenteType}&year=${route.params.gemeenteYear}&video=${route.params.videoID}.mp4`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch video');
        }
        return response.blob();
    })
    .then(blob => {
        videoUrl.value = URL.createObjectURL(blob);
        console.log(videoUrl.value)
    })
    .catch(error => {
        console.error('Error fetching video:', error);
    });

fetch(`http://127.0.0.1:3012/api/getSpeakers?gemeente=${route.params.gemeenteName}&meetingType=${route.params.gemeenteType}&year=${route.params.gemeenteYear}&video=${route.params.videoID}.mp4`)
.then(response => response.json())
.then(data => {
    speakers.value = data.speakers
    createSpeakerMapping()
    createSpeakerNameMapping()
})

// fetch(`http://127.0.0.1:3012/api/getTranscript?gemeente=${route.params.gemeenteName}&meetingType=${route.params.gemeenteType}&year=${route.params.gemeenteYear}&video=${route.params.videoID}.mp4`)
// .then(response => response.json())
// .then(data => {
//     transcript.value = data.transcript
// })

fetch(`http://127.0.0.1:3012/api/getAgenda?gemeente=${route.params.gemeenteName}&meetingType=${route.params.gemeenteType}&year=${route.params.gemeenteYear}&video=${route.params.videoID}.mp4`)
.then(response => response.json())
.then(data => {
    var total = 0;
    agenda.value = data.agenda.map(function (obj) {
        if (obj.time != null) {
            const seconds = HMStoSeconds(obj.time)
            total = total + seconds
            return { agendaPoint: obj.agendaPoint, time: seconds, start: total-seconds }
        } else {
            return { agendaPoint: obj.agendaPoint }
        }
    })
    createAgendaMapping()
    console.log("agenda", agenda.value)
})

const hrWidth = computed(() => videoDuration.value * 1)

const availableSpeakerColors = ['bg-red-600', 'bg-red-700', 'bg-red-800', 'bg-red-900', 'bg-orange-600', 'bg-orange-700', 'bg-orange-800', 'bg-orange-900', 'bg-amber-600', 'bg-amber-700', 'bg-amber-800', 'bg-amber-900', 'bg-lime-600', 'bg-lime-700', 'bg-lime-800', 'bg-lime-900', 'bg-emerald-600', 'bg-emerald-700', 'bg-emerald-800', 'bg-emerald-900', 'bg-pink-600', 'bg-pink-700', 'bg-pink-800', 'bg-pink-900', 'bg-rose-600', 'bg-rose-700', 'bg-rose-800', 'bg-rose-900']
const availableAgendaColors = ['bg-red-600', 'bg-red-700', 'bg-red-800', 'bg-red-900', 'bg-orange-600', 'bg-orange-700', 'bg-orange-800', 'bg-orange-900', 'bg-amber-600', 'bg-amber-700', 'bg-amber-800', 'bg-amber-900', 'bg-lime-600', 'bg-lime-700', 'bg-lime-800', 'bg-lime-900', 'bg-emerald-600', 'bg-emerald-700', 'bg-emerald-800', 'bg-emerald-900', 'bg-pink-600', 'bg-pink-700', 'bg-pink-800', 'bg-pink-900', 'bg-rose-600', 'bg-rose-700', 'bg-rose-800', 'bg-rose-900']

function createSpeakerMapping() {
    if (!speakers.value) return
    speakers.value.forEach(speaker => {
        if (!(speaker.speaker in speakerColors.value) && speaker.speaker != "") {
            speakerColors.value[speaker.speaker] = getRandomSpeakerColor();
        }
    });
}

async function getSpeakerName(speakerID) {
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: route.params.videoID, speakerID: speakerID })
    };
    const nameResponse = await fetch(`http://127.0.0.1:3012/api/weaviate/getSpeakerName`, options)
    const data = await nameResponse.json();

    return data.name
}

function getRandomSuffix() {
    let result = '';
    for (let i = 0; i < 5; i++) {
        result += Math.floor(Math.random() * 10);
    }
    return result;
}

async function createSpeakerNameMapping() {
    if (!speakers.value) return
    let promises = [];
    speakers.value.forEach(async speaker => {
        if (speaker.speaker != "") {
            if (!(speaker.speaker in speakerNameMapping.value)) {
                speakerNameMapping.value[speaker.speaker] = ""
                let namePromise = getSpeakerName(speaker.speaker);
                promises.push(namePromise.then(name => {
                    if (name === "inspreker") {
                        name = "inspreker" + getRandomSuffix()
                    }
                    speaker.name = name
                    speakerNameMapping.value[speaker.speaker] = name
                }));
            }
        }
    });
    // Wait for requests to finish and then name all unnnamed speakers.
    await Promise.all(promises)
    speakers.value.forEach(speaker => {
        speaker.name = speakerNameMapping.value[speaker.speaker]
    })
}

function createAgendaMapping() {
    if (!agenda.value) return
    agenda.value.forEach(a => {
        if (!(a.agendaPoint in agendaColors.value) && a.agendaPoint != "") {
            agendaColors.value[a.agendaPoint] = getRandomAgendaColor();
        }
    });
}

function getRandomSpeakerColor() {
    if (availableSpeakerColors.length == 0) {
        console.log("ERROR! no more speaker colors left, too many speakers.")
    }
    const randomIndex = Math.floor(Math.random() * availableSpeakerColors.length-1 )
    const c = availableSpeakerColors.splice(randomIndex, 1)[0]
    return c
}

function getRandomAgendaColor() {
    if (availableAgendaColors.length == 0) {
        console.log("ERROR! no more agenda colors left, too many agenda punten.")
    }
    const randomIndex = Math.floor(Math.random() * availableAgendaColors.length-1 )
    const c = availableAgendaColors.splice(randomIndex, 1)[0]
    return c
}

function updateLinePosition(event) {
    isHovering.value = true;
    lineLeft.value = event.clientX - event.target.getBoundingClientRect().left;
}

function resetLinePosition() {
    isHovering.value = false;
}

function secondsToHMS(seconds) {
    var hours = Math.floor(seconds / 3600);
    var minutes = Math.floor((seconds % 3600) / 60);
    var remainingSeconds = seconds % 60;

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    remainingSeconds = (remainingSeconds < 10) ? "0" + remainingSeconds : remainingSeconds;

    return hours + ':' + minutes + ':' + Math.round(remainingSeconds);
}

function HMStoSeconds(timeString) {
    var timeParts = timeString.split(':');

    var hours = parseInt(timeParts[0]);
    var minutes = parseInt(timeParts[1]);
    var seconds = parseInt(timeParts[2]);

    var totalSeconds = (hours * 3600) + (minutes * 60) + seconds;

    return totalSeconds;
}

function goToVideoPosition() {
    console.log(`Not implemented, going to video position ${lineLeft.value} seconds, which is ${secondsToHMS(lineLeft.value)}`)
    const video = document.getElementById("videoPlayer")
    video.currentTime = lineLeft.value
}

function isOffset() {
    if (!speakers.value) return false
    if (speakers.value.length == 0) return false
    else return speakers.value[0].start > 0
}

function goToOriginalVideo() {
    if (route.params.gemeenteName == "hoekschewaard") {
        const url = `https://hoekschewaard.notubiz.nl/vergadering/${route.params.videoID}`;
        window.open(url, '_blank')
    } else {
        console.log("TODO: GOTO", route.params.gemeenteName)
    }
}

async function downloadInfo() {
    const resp = await fetch(`http://127.0.0.1:3012/api/downloadArchive?gemeente=${route.params.gemeenteName}&meetingType=${route.params.gemeenteType}&year=${route.params.gemeenteYear}&video=${route.params.videoID}.mp4`)
    if (!resp.ok) {
        console.error('Failed to fetch the file:', resp.statusText);
        return;
    }
    const blob = await resp.blob();
    console.log('Blob size:', blob.size);
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${route.params.videoID}.zip`);
    document.body.appendChild(link);
    link.click();

    // Cleanup
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

</script>

<template>
    <div class="flex flex-col">
        <div class="flex flex-row flex-grow">
            <div class="flex justify-center flex-col mx-4 self-start flex-grow">
                <h1 class="text-5xl hover:cursor-pointer" @click="goToOriginalVideo()"> {{ route.params.gemeenteName }}
                    video {{
                    route.params.videoID }}.mp4
                </h1>
                <button @click="downloadInfo()" >Download information</button>
                <div class="my-6 max-w-4xl flex flex-col justify-center">
                    <video v-if="videoUrl" id="videoPlayer" controls preload="auto">
                        <source :src="videoUrl" type="video/mp4">
                        </source>
                        <p class="vjs-no-js">
                            To view this video please enable JavaScript, and consider upgrading to a
                            web browser that
                            <a href="https://videojs.com/html5-video-support/" target="_blank">
                                supports HTML5 video
                            </a>
                        </p>
                    </video>
                    <span v-else>
                        video is loading...
                    </span>

                    <div class="relative overflow-auto my-6">
                        <div class="absolute top-0 bg-white h-8 w-px ml-1"
                            :style="{ left: lineLeft + 'px', display: isHovering ? 'block' : 'none' }">
                            ~{{ secondsToHMS(lineLeft) }}
                        </div>

                        <div>
                            <div :style="{ width: hrWidth + 'px' }" class="flex flex-row flex-nowrap mb-2">
                                <hr v-for="a in agenda" :style="{ width: a.time + 'px' }"
                                    class=" h-3 border-0 rounded" :class="agendaColors[a.agendaPoint]"
                                    :title="a.agendaPoint">
                            </div>

                            <div :style="{ width: hrWidth + 'px' }" class="flex flex-row flex-nowrap mb-2">
                                <hr v-if="isOffset()" :style="{ width: speakers[0].start + 'px' }"
                                    class=" h-3 border-0 rounded bg-transparent">
                                <hr v-for="s in speakers" :style="{ width: s.end-s.start + 'px' }"
                                    class=" h-3 border-0 rounded" :class="speakerColors[s.speaker]" :title="s.name">
                            </div>

                            <div @mousemove="updateLinePosition" @mouseleave="resetLinePosition"
                                @click="goToVideoPosition" class="pb-4">
                                <hr :style="{ width: hrWidth + 'px' }" class="h-3 border-0 rounded dark:bg-gray-700">
                            </div>
                        </div>
                    </div>

                    <SearchVideo v-if="speakers.length>0" :speakers="speakers" :agenda="agenda" class="my-4"></SearchVideo>
                </div>

            </div>
            <div class="flex flex-col ">
                <AgendaPoints :agenda="agenda" class="mx-4 my-2"></AgendaPoints>

                <VideoChat class="mx-4 my-2"></VideoChat>
            </div>

        </div>
    </div>

</template>
