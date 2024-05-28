<script setup>
import { ref } from 'vue';

import SearchBar from "../components/SearchBar.vue"
import SearchSettings from '../components/SearchSettings.vue';
import Results from '../components/Results.vue';

const searchQuery = ref("")
const gemeentes = ref([]);
const searchAlpha = ref(0.5);
const searchLimit = ref(10);
const searchMethod = ref("vector");
const searchGemeente = ref("");
const searchType = ref("");
const searchYear = ref("");
const searchSpeaker = ref("");
const searchVideoID = ref("");

const searchResults = ref([]);


fetch('http://127.0.0.1:3012/api/gemeentes')
    .then(response => response.json())
    .then(data => gemeentes.value = data.gemeentes)


function updateSearchGemeente(emittedValue) {
    searchGemeente.value = emittedValue
}

function updateSearchType(emittedValue) {
    searchType.value = emittedValue
}

function updateSearchYear(emittedValue) {
    searchYear.value = emittedValue
}

function updateSearchSpeaker(emittedValue) {
    searchSpeaker.value = emittedValue
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

function HandleNewQueryEmit(query) {
    searchQuery.value = query
}

</script>

<template>
    <div class="flex flex-col">
        <SearchBar :limit="searchLimit" :alpha="searchAlpha" :method="searchMethod" :gemeente="searchGemeente"
            :type="searchType" :year="searchYear" :speaker="searchSpeaker" :video="searchVideoID" :minTime=-1
            :maxTime=-1 @newResults="updateResults" @newQuery="HandleNewQueryEmit" />
        <SearchSettings :searchGemeenteActive="true" :searchTypeActive="true" :searchYearActive="true"
            :availableSpeakersProp="[]" :gemeentes="gemeentes" @newGemeenteToSearch="updateSearchGemeente"
            @newMeetingTypeToSearch="updateSearchType" @newMeetingYearToSearch="updateSearchYear"
            @newSpeakerToSearch="updateSearchSpeaker" @newSearchMethod="updateSearchMethod"
            @newSearchLimit="updateSearchLimit" @newSearchalpha="updateSearchAlpha" />
        <Results :query="searchQuery" :results="searchResults"></Results>
    </div>
</template>