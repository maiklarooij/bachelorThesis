<script setup>
import ResultCard from './ResultCard.vue';

const props = defineProps({
    query: String,
    results: Array,
    speakers: Array,
})

function getSpeakerName(speakerID) {
    for (let i = 0; i < props.speakers.length; i++) {
        if (props.speakers[i].speaker === speakerID) {
            return props.speakers[i].name;
        }
    }
    return speakerID
}

</script>

<template>
    <ResultCard v-for="r in results" :query="query" :code="r.properties.code" :text="r.properties.text"
        :start="r.properties.start" :end="r.properties.end" :year="r.properties.year"
        :government="r.properties.government" :type="r.properties.type" :speaker="getSpeakerName(r.properties.speaker)"
        :distance="r.score">
    </ResultCard>
    <span v-if="results.length == 0">No search results</span>
</template>
