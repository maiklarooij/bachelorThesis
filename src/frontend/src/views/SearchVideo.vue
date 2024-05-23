<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'

import SearchBar from "../components/SearchBar.vue"
import SearchSettings from '../components/SearchSettings.vue';
import ResultsVideo from '../components/ResultsVideo.vue';

const route = useRoute()

const props = defineProps({
    speakers: Array,
    agenda: Array,
})

const searchQuery = ref("")
const gemeentes = ref([]);
const searchAlpha = ref(0.5);
const searchLimit = ref(10);
const searchMethod = ref("vector");
const searchGemeente = ref(route.params.gemeenteName);
const searchType = ref(route.params.gemeenteType);
const searchYear = ref(route.params.gemeenteYear);
const searchVideoID = ref(route.params.videoID);
const searchSpeaker = ref("");
const searchMinTime = ref(-1);
const searchMaxTime = ref(-1);

const searchResults = ref([]);

function updateSearchSpeaker(emittedValue) {
    // Finds the speaker property of the object whose name is emittedValue
    searchSpeaker.value = props.speakers.find(obj => obj.name === emittedValue).speaker
}

function updateSearchMethod(emittedValue) {
    searchMethod.value = emittedValue
}

function updateResults(emittedValue) {
    searchResults.value = emittedValue
}

function updateSearchLimit(emittedValue) {
    searchLimit.value = emittedValue
}

function updateSearchAlpha(emittedValue) {
    searchAlpha.value = emittedValue
}

function updateSearchAgendaTime(startTime, endTime) {
    console.log(startTime, endTime)
    searchMinTime.value = startTime
    searchMaxTime.value = endTime
}

function filterSpeakers() {
    if (!props.speakers) return
    return [...new Set(props.speakers.map(obj => obj.name))]
    // return [...new Set(props.speakers.map(obj => obj.speaker))]
}

function HandleNewQueryEmit(query) {
    searchQuery.value = query
}

</script>

<template>
    <div class="flex flex-col">
        <SearchBar :limit="searchLimit" :alpha="searchAlpha" :method="searchMethod" :gemeente="searchGemeente"
            :type="searchType" :year="searchYear" :speaker="searchSpeaker" :video="searchVideoID"
            :minTime="searchMinTime" :maxTime="searchMaxTime" @newResults="updateResults"
            @newQuery="HandleNewQueryEmit" />
        <SearchSettings :searchGemeenteActive="false" :searchTypeActive="false" :searchYearActive="false"
            :availableAgenda="agenda" :gemeentes="gemeentes" :availableSpeakersProp="filterSpeakers()"
            @newSpeakerToSearch="updateSearchSpeaker" @newSearchMethod="updateSearchMethod"
            @newSearchLimit="updateSearchLimit" @newSearchalpha="updateSearchAlpha" @newAgendaToSearch="updateSearchAgendaTime"/>
        <ResultsVideo :query="searchQuery" :speakers="speakers" :results="searchResults"></ResultsVideo>
    </div>
</template>
